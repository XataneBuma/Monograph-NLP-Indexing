import reflex as rx
import asyncio
from typing import TypedDict
import datetime
import random
import pymupdf
import yake
import spacy
import numpy as np
import hashlib
import os
import logging
import faiss


class DocumentEntity(TypedDict):
    text: str
    label: str


class Document(TypedDict):
    id: str
    title: str
    author: str
    upload_date: str
    file_path: str
    status: str
    pipeline_stage: int
    extracted_text: str
    keywords: list[str]
    entities: list[DocumentEntity]
    embedding: list[float]
    score: float


class DocumentState(rx.State):
    documents: list[Document] = [
        {
            "id": "101",
            "title": "Semantic Indexing Foundations",
            "author": "Dr. A. Smith",
            "upload_date": "2024-05-01",
            "file_path": "doc1.pdf",
            "status": "completed",
            "pipeline_stage": 3,
            "extracted_text": "Semantic indexing improves information retrieval by focusing on the meaning of words rather than just their literal string matching. This monograph explores various techniques...",
            "keywords": ["semantic", "indexing", "nlp", "retrieval"],
            "entities": [
                {"text": "Dr. A. Smith", "label": "PERSON"},
                {"text": "MIT", "label": "ORG"},
            ],
            "embedding": [],
        },
        {
            "id": "102",
            "title": "Advanced OCR Techniques",
            "author": "J. Doe",
            "upload_date": "2024-05-02",
            "file_path": "doc2.pdf",
            "status": "processing",
            "pipeline_stage": 1,
            "extracted_text": "Optical Character Recognition (OCR) is the electronic or mechanical conversion of images of typed, handwritten or printed text into machine-encoded text...",
            "keywords": [],
            "entities": [],
            "embedding": [],
        },
        {
            "id": "103",
            "title": "Neural Networks in 2024",
            "author": "K. Lee",
            "upload_date": "2024-05-10",
            "file_path": "doc3.pdf",
            "status": "uploaded",
            "pipeline_stage": 0,
            "extracted_text": "",
            "keywords": [],
            "entities": [],
            "embedding": [],
        },
    ]
    current_view: str = "dashboard"
    selected_document_id: str = ""
    is_uploading: bool = False
    view_mode: str = "grid"
    search_query: str = ""
    semantic_search_query: str = ""
    search_results: list[Document] = []
    related_documents: list[Document] = []
    processing_queue: list[str] = []
    is_processing_queue_running: bool = False
    is_sidebar_open: bool = False

    @rx.var
    def stats_total_documents(self) -> int:
        return len(self.documents)

    @rx.var
    def stats_processing(self) -> int:
        return len([d for d in self.documents if d["status"] == "processing"])

    @rx.var
    def stats_completed(self) -> int:
        return len([d for d in self.documents if d["status"] == "completed"])

    @rx.var
    def filtered_documents(self) -> list[Document]:
        if not self.search_query:
            return self.documents
        query = self.search_query.lower()
        return [
            d
            for d in self.documents
            if query in d["title"].lower() or query in d["author"].lower()
        ]

    @rx.var
    def selected_document(self) -> Document:
        found = [d for d in self.documents if d["id"] == self.selected_document_id]
        if found:
            return found[0]
        return {
            "id": "0",
            "title": "No Document Selected",
            "author": "-",
            "upload_date": "-",
            "file_path": "",
            "status": "uploaded",
            "pipeline_stage": 0,
            "extracted_text": "No content available.",
            "keywords": [],
            "entities": [],
            "embedding": [],
            "score": 0.0,
        }

    @rx.event
    def set_view(self, view: str):
        self.current_view = view
        self.is_sidebar_open = False

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def close_sidebar(self):
        self.is_sidebar_open = False

    @rx.event
    def select_document(self, doc_id: str):
        self.selected_document_id = doc_id
        self.current_view = "detail"
        self.find_related_documents()

    @rx.event
    def toggle_view_mode(self):
        self.view_mode = "list" if self.view_mode == "grid" else "grid"

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_semantic_search_query(self, query: str):
        self.semantic_search_query = query

    def _generate_embedding(self, text: str) -> list[float]:
        """Generates a mock embedding using the same hash-based strategy as the pipeline."""
        dim = 128
        vec = np.zeros(dim)
        words = text.lower().split()
        if not words:
            return vec.tolist()
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16) % dim
            vec[h] += 1
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def _compute_hybrid_search(
        self, query_text: str, top_k: int = 5, exclude_id: str = None
    ) -> list[Document]:
        completed_docs = [
            d
            for d in self.documents
            if d["status"] == "completed" and d.get("embedding")
        ]
        if not completed_docs:
            return []
        dim = 128
        embeddings = np.array([d["embedding"] for d in completed_docs]).astype(
            "float32"
        )
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        query_embedding = np.array([self._generate_embedding(query_text)]).astype(
            "float32"
        )
        D, I = index.search(query_embedding, len(completed_docs))
        query_terms = set(query_text.lower().split())
        scored_docs = []
        max_distance = np.max(D) if np.max(D) > 0 else 1.0
        for rank, idx in enumerate(I[0]):
            doc = completed_docs[idx]
            if exclude_id and doc["id"] == exclude_id:
                continue
            distance = D[0][rank]
            vector_score = 1 - distance / max_distance
            text_lower = doc["extracted_text"].lower()
            term_matches = sum((1 for term in query_terms if term in text_lower))
            keyword_score = term_matches / len(query_terms) if query_terms else 0
            final_score = 0.7 * vector_score + 0.3 * keyword_score
            doc_copy = doc.copy()
            doc_copy["score"] = final_score
            scored_docs.append(doc_copy)
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]

    @rx.event
    def perform_semantic_search(self):
        if not self.semantic_search_query.strip():
            self.search_results = []
            return
        self.search_results = self._compute_hybrid_search(
            self.semantic_search_query, top_k=10
        )

    @rx.event
    def find_related_documents(self):
        current_doc = self.selected_document
        if current_doc["status"] != "completed":
            self.related_documents = []
            return
        query_preview = current_doc["extracted_text"][:500]
        self.related_documents = self._compute_hybrid_search(
            query_preview, top_k=4, exclude_id=current_doc["id"]
        )

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_uploading = True
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        queue_trigger = False
        for file in files:
            data = await file.read()
            unique_name = f"{datetime.datetime.now().timestamp()}_{file.name}"
            file_path = upload_dir / unique_name
            with file_path.open("wb") as f:
                f.write(data)
            new_id = str(random.randint(10000, 99999))
            new_doc: Document = {
                "id": new_id,
                "title": file.name,
                "author": "Unknown Author",
                "upload_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "file_path": unique_name,
                "status": "uploaded",
                "pipeline_stage": 0,
                "extracted_text": "",
                "keywords": [],
                "entities": [],
                "embedding": [],
                "score": 0.0,
            }
            self.documents.insert(0, new_doc)
            self.processing_queue.append(new_id)
            queue_trigger = True
        self.is_uploading = False
        yield rx.toast.success(f"Uploaded {len(files)} files successfully!")
        if queue_trigger and (not self.is_processing_queue_running):
            self.is_processing_queue_running = True
            yield DocumentState.process_next_document

    @rx.event(background=True)
    async def process_next_document(self):
        async with self:
            if not self.processing_queue:
                self.is_processing_queue_running = False
                return
            doc_id = self.processing_queue[0]
            current_doc_idx = next(
                (i for i, d in enumerate(self.documents) if d["id"] == doc_id), -1
            )
            if current_doc_idx == -1:
                self.processing_queue.pop(0)
                return
            self.documents[current_doc_idx]["status"] = "processing"
            self.documents[current_doc_idx]["pipeline_stage"] = 1
            self.documents[current_doc_idx]["extracted_text"] = (
                "Extracting text from PDF..."
            )
        try:
            upload_dir = rx.get_upload_dir()
            async with self:
                filename = self.documents[current_doc_idx]["file_path"]
            file_path = upload_dir / filename
            extracted_text = ""
            try:
                doc = pymupdf.open(file_path)
                for page in doc:
                    extracted_text += (
                        page.get_text()
                        + """
"""
                    )
                doc.close()
            except Exception as e:
                logging.exception(f"PDF Extraction Error: {e}")
                extracted_text = f"Error extracting text: {str(e)}"
                async with self:
                    self.documents[current_doc_idx]["status"] = "failed"
                    self.documents[current_doc_idx]["extracted_text"] = extracted_text
                    self.processing_queue.pop(0)
                return
            if not extracted_text.strip():
                extracted_text = "No text could be extracted from this document (it might be an image scan without OCR layer)."
            async with self:
                self.documents[current_doc_idx]["extracted_text"] = extracted_text
                self.documents[current_doc_idx]["pipeline_stage"] = 2
            keywords = []
            try:
                kw_extractor = yake.KeywordExtractor(
                    lan="pt", n=2, dedupLim=0.9, top=10, features=None
                )
                keywords_extracted = kw_extractor.extract_keywords(extracted_text)
                keywords = [k[0] for k in keywords_extracted]
            except Exception as e:
                logging.exception(f"YAKE Error: {e}")
                keywords = ["Processing Error"]
            async with self:
                self.documents[current_doc_idx]["keywords"] = keywords
                self.documents[current_doc_idx]["pipeline_stage"] = 3
            entities = []
            try:
                try:
                    nlp = spacy.load("pt_core_news_sm")
                except Exception as e:
                    logging.exception(f"Spacy load error: {e}")
                    nlp = spacy.blank("pt")
                doc_nlp = nlp(extracted_text[:100000])
                seen_entities = set()
                for ent in doc_nlp.ents:
                    if (
                        ent.label_ in ["PER", "ORG", "LOC", "MISC", "DATE"]
                        and ent.text not in seen_entities
                    ):
                        entities.append({"text": ent.text, "label": ent.label_})
                        seen_entities.add(ent.text)
                if (
                    not self.documents[current_doc_idx]["author"]
                    or self.documents[current_doc_idx]["author"] == "Unknown Author"
                ):
                    authors = [e["text"] for e in entities if e["label"] == "PER"]
                    if authors:
                        async with self:
                            self.documents[current_doc_idx]["author"] = authors[0]
            except Exception as e:
                logging.exception(f"NER Error: {e}")
            embedding = []
            try:
                dim = 128
                vec = np.zeros(dim)
                words = extracted_text.lower().split()
                for word in words:
                    h = int(hashlib.md5(word.encode()).hexdigest(), 16) % dim
                    vec[h] += 1
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
                embedding = vec.tolist()
            except Exception as e:
                logging.exception(f"Embedding Error: {e}")
                embedding = [0.0] * 128
            async with self:
                self.documents[current_doc_idx]["entities"] = entities[:20]
                self.documents[current_doc_idx]["embedding"] = embedding
                self.documents[current_doc_idx]["status"] = "completed"
                self.documents[current_doc_idx]["pipeline_stage"] = 3
                self.processing_queue.pop(0)
            yield DocumentState.process_next_document
        except Exception as e:
            logging.exception(f"Critical Pipeline Error: {e}")
            async with self:
                if self.processing_queue:
                    self.processing_queue.pop(0)
            yield DocumentState.process_next_document