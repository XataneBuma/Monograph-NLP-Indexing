import reflex as rx
from app.states.document_state import DocumentState, Document


def search_result_card(doc: Document) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    doc["title"],
                    class_name="text-lg font-semibold text-indigo-700 cursor-pointer hover:underline",
                    on_click=lambda: DocumentState.select_document(doc["id"]),
                ),
                rx.el.span(
                    f"{doc['score'] * 100:.0f}% Match",
                    class_name="text-xs font-bold px-2 py-1 bg-green-100 text-green-700 rounded-full",
                ),
                class_name="flex justify-between items-start mb-1",
            ),
            rx.el.p(
                f"By {doc['author']} • {doc['upload_date']}",
                class_name="text-sm text-gray-500 mb-3",
            ),
            rx.el.p(
                doc["extracted_text"][:250] + "...",
                class_name="text-sm text-gray-600 leading-relaxed mb-3 line-clamp-3",
            ),
            rx.el.div(
                rx.foreach(
                    doc["keywords"][:4],
                    lambda k: rx.el.span(
                        f"#{k}",
                        class_name="text-xs text-indigo-500 bg-indigo-50 px-2 py-1 rounded-md font-medium",
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200",
    )


def search_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Semantic Search", class_name="text-2xl font-bold text-gray-800 mb-2"
            ),
            rx.el.p(
                "Find monographs based on meaning and context, not just keywords.",
                class_name="text-gray-500 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 text-indigo-500 h-6 w-6",
                    ),
                    rx.el.input(
                        placeholder="Describe the research topic, methodology, or concepts you are looking for...",
                        on_change=DocumentState.set_semantic_search_query,
                        class_name="w-full pl-14 pr-32 py-4 text-lg border-2 border-indigo-100 rounded-2xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/20 outline-none transition-all shadow-sm",
                        default_value=DocumentState.semantic_search_query,
                    ),
                    rx.el.button(
                        "Search",
                        on_click=DocumentState.perform_semantic_search,
                        class_name="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-colors shadow-sm",
                    ),
                    class_name="relative w-full max-w-4xl mx-auto",
                ),
                class_name="w-full mb-12",
            ),
            rx.cond(
                DocumentState.search_results,
                rx.el.div(
                    rx.el.h3(
                        f"Top {DocumentState.search_results.length()} Results",
                        class_name="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(DocumentState.search_results, search_result_card),
                        class_name="grid grid-cols-1 gap-6 max-w-4xl mx-auto",
                    ),
                    class_name="w-full animate-in fade-in slide-in-from-bottom-4 duration-500",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "brain-circuit", class_name="h-16 w-16 text-gray-200 mb-4"
                        ),
                        rx.el.p(
                            "Enter a natural language query to start searching.",
                            class_name="text-gray-400 font-medium",
                        ),
                        class_name="flex flex-col items-center justify-center py-20",
                    ),
                    class_name="w-full border-2 border-dashed border-gray-100 rounded-2xl",
                ),
            ),
            class_name="flex flex-col w-full max-w-6xl mx-auto",
        ),
        class_name="p-4 md:p-8 w-full min-h-full",
    )