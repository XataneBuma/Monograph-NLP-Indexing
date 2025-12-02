import reflex as rx
from app.states.document_state import DocumentState


def stage_indicator(label: str, stage_num: int, current_stage: int) -> rx.Component:
    status_color = rx.cond(
        stage_num < current_stage,
        "bg-green-500 border-green-500 text-white",
        rx.cond(
            stage_num == current_stage,
            "bg-blue-600 border-blue-600 text-white animate-pulse",
            "bg-white border-gray-300 text-gray-400",
        ),
    )
    line_color = rx.cond(stage_num < current_stage, "bg-green-500", "bg-gray-200")
    return rx.el.div(
        rx.cond(
            stage_num < 3,
            rx.el.div(
                class_name=f"absolute top-4 left-1/2 w-full h-0.5 -z-10 {line_color}"
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.match(
                stage_num < current_stage,
                (True, rx.icon("check", size=16)),
                (False, rx.el.span(stage_num + 1, class_name="text-xs font-bold")),
            ),
            class_name=f"w-8 h-8 rounded-full flex items-center justify-center border-2 {status_color} transition-colors duration-300 z-10 relative",
        ),
        rx.el.span(label, class_name="mt-2 text-xs font-medium text-gray-600"),
        class_name="flex flex-col items-center relative flex-1",
    )


def document_detail() -> rx.Component:
    doc = DocumentState.selected_document
    return rx.el.div(
        rx.el.button(
            rx.icon("arrow-left", size=16),
            "Back to Library",
            on_click=lambda: DocumentState.set_view("library"),
            class_name="flex items-center gap-2 text-gray-500 hover:text-gray-800 mb-6 text-sm font-medium transition-colors",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            doc["title"],
                            class_name="text-2xl font-bold text-gray-900 mb-2",
                        ),
                        rx.el.p(f"By {doc['author']}", class_name="text-gray-600"),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Processing Pipeline",
                            class_name="text-sm font-semibold text-gray-900 mb-4 uppercase tracking-wider",
                        ),
                        rx.el.div(
                            stage_indicator("Uploaded", 0, doc["pipeline_stage"]),
                            stage_indicator("OCR Extraction", 1, doc["pipeline_stage"]),
                            stage_indicator("NLP Analysis", 2, doc["pipeline_stage"]),
                            stage_indicator("Indexed", 3, doc["pipeline_stage"]),
                            class_name="flex justify-between w-full relative px-4",
                        ),
                        class_name="bg-gray-50 p-6 rounded-xl border border-gray-200 mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Extracted Content",
                                class_name="text-lg font-semibold text-gray-800",
                            ),
                            rx.el.button(
                                rx.icon("copy", size=16),
                                class_name="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100",
                            ),
                            class_name="flex items-center justify-between mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                doc["extracted_text"],
                                class_name="text-gray-700 leading-relaxed whitespace-pre-wrap",
                            ),
                            class_name="bg-white p-6 rounded-xl border border-gray-200 min-h-[300px] shadow-sm",
                        ),
                        class_name="mt-8",
                    ),
                    class_name="col-span-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Metadata",
                            class_name="text-lg font-semibold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "Upload Date",
                                    class_name="text-xs text-gray-500 uppercase",
                                ),
                                rx.el.p(
                                    doc["upload_date"],
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "File Name",
                                    class_name="text-xs text-gray-500 uppercase",
                                ),
                                rx.el.p(
                                    doc["file_path"],
                                    class_name="text-sm font-medium text-gray-900 truncate",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Document ID",
                                    class_name="text-xs text-gray-500 uppercase",
                                ),
                                rx.el.p(
                                    doc["id"],
                                    class_name="text-sm font-medium text-gray-900 font-mono",
                                ),
                                class_name="mb-4",
                            ),
                            class_name="space-y-2",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Keywords",
                            class_name="text-lg font-semibold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                doc["keywords"],
                                lambda keyword: rx.el.span(
                                    keyword,
                                    class_name="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-sm font-medium",
                                ),
                            ),
                            rx.cond(
                                doc["keywords"],
                                rx.fragment(),
                                rx.el.p(
                                    "No keywords extracted yet.",
                                    class_name="text-sm text-gray-400 italic",
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Detected Entities",
                            class_name="text-lg font-semibold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                doc["entities"],
                                lambda entity: rx.el.div(
                                    rx.el.span(
                                        entity["text"],
                                        class_name="text-sm font-medium text-gray-800",
                                    ),
                                    rx.el.span(
                                        entity["label"],
                                        class_name="text-xs font-bold text-gray-500 bg-gray-100 px-2 py-0.5 rounded",
                                    ),
                                    class_name="flex items-center justify-between py-2 border-b border-gray-100 last:border-0",
                                ),
                            ),
                            rx.cond(
                                doc["entities"],
                                rx.fragment(),
                                rx.el.p(
                                    "No entities detected yet.",
                                    class_name="text-sm text-gray-400 italic",
                                ),
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
            rx.cond(
                DocumentState.related_documents,
                rx.el.div(
                    rx.el.h3(
                        "Related Works",
                        class_name="text-xl font-bold text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DocumentState.related_documents,
                            lambda doc: rx.el.div(
                                rx.el.div(
                                    rx.el.h4(
                                        doc["title"],
                                        class_name="font-semibold text-gray-900 mb-1 line-clamp-1",
                                    ),
                                    rx.el.p(
                                        f"By {doc['author']}",
                                        class_name="text-sm text-gray-500 mb-3",
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            f"{doc['score'] * 100:.0f}% Match",
                                            class_name="text-xs font-bold px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-full",
                                        ),
                                        rx.el.button(
                                            "View",
                                            on_click=lambda: DocumentState.select_document(
                                                doc["id"]
                                            ),
                                            class_name="text-sm text-indigo-600 hover:text-indigo-800 font-medium",
                                        ),
                                        class_name="flex items-center justify-between",
                                    ),
                                    class_name="flex flex-col h-full",
                                ),
                                class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200",
                            ),
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
                    ),
                    class_name="mt-12 pt-8 border-t border-gray-200",
                ),
                rx.fragment(),
            ),
            class_name="max-w-7xl mx-auto",
        ),
        class_name="p-4 md:p-8 w-full",
    )