import reflex as rx
from app.states.document_state import DocumentState, Document


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "completed",
            rx.el.span(
                "Indexed",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
        ),
        (
            "processing",
            rx.el.span(
                "Processing",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 animate-pulse",
            ),
        ),
        (
            "uploaded",
            rx.el.span(
                "Uploaded",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
        ),
        (
            "failed",
            rx.el.span(
                "Failed",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
        ),
        rx.el.span(
            status,
            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def document_card(doc: Document) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="h-8 w-8 text-indigo-600 mb-4"),
            rx.el.div(status_badge(doc["status"]), class_name="absolute top-4 right-4"),
            class_name="relative",
        ),
        rx.el.h4(
            doc["title"], class_name="font-semibold text-gray-900 mb-1 line-clamp-1"
        ),
        rx.el.p(doc["author"], class_name="text-sm text-gray-500 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.span("Uploaded:", class_name="text-xs text-gray-400"),
                rx.el.span(
                    doc["upload_date"], class_name="text-xs font-medium text-gray-600"
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.button(
                "View Details",
                on_click=lambda: DocumentState.select_document(doc["id"]),
                class_name="w-full py-2 px-3 bg-gray-50 hover:bg-indigo-50 text-indigo-600 text-sm font-medium rounded-lg transition-colors border border-gray-100 hover:border-indigo-200",
            ),
            class_name="mt-auto",
        ),
        class_name="flex flex-col p-5 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200",
    )


def document_row(doc: Document) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("file-text", class_name="h-5 w-5 text-indigo-600"),
                rx.el.span(doc["title"], class_name="font-medium text-gray-900"),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            doc["author"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            doc["upload_date"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(status_badge(doc["status"]), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.el.button(
                "View",
                on_click=lambda: DocumentState.select_document(doc["id"]),
                class_name="text-indigo-600 hover:text-indigo-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def library_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search by title or author...",
                        on_change=DocumentState.set_search_query,
                        class_name="pl-10 pr-4 py-2 w-full border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all",
                        default_value=DocumentState.search_query,
                    ),
                    class_name="relative w-full md:w-96",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("layout-grid", class_name="h-5 w-5"),
                        on_click=DocumentState.toggle_view_mode,
                        class_name=rx.cond(
                            DocumentState.view_mode == "grid",
                            "p-2 bg-gray-100 text-gray-800 rounded-lg",
                            "p-2 text-gray-400 hover:text-gray-600",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("list", class_name="h-5 w-5"),
                        on_click=DocumentState.toggle_view_mode,
                        class_name=rx.cond(
                            DocumentState.view_mode == "list",
                            "p-2 bg-gray-100 text-gray-800 rounded-lg",
                            "p-2 text-gray-400 hover:text-gray-600",
                        ),
                    ),
                    class_name="flex items-center gap-1 border-l border-gray-200 pl-4 ml-4",
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
        ),
        rx.cond(
            DocumentState.view_mode == "grid",
            rx.el.div(
                rx.foreach(DocumentState.filtered_documents, document_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Document",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Author",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Uploaded",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th("", class_name="px-6 py-3 relative"),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(DocumentState.filtered_documents, document_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg",
            ),
        ),
        class_name="p-4 md:p-8 w-full",
    )