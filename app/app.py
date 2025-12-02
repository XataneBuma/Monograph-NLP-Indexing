import reflex as rx
from app.states.document_state import DocumentState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.upload_area import upload_area
from app.components.document_list import library_view
from app.components.document_detail import document_detail
from app.components.search_view import search_view


def dashboard_widgets() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Total Documents", class_name="text-sm font-medium text-gray-500"
                ),
                rx.el.p(
                    DocumentState.stats_total_documents,
                    class_name="text-3xl font-bold text-gray-900 mt-2",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3("Processing", class_name="text-sm font-medium text-gray-500"),
                rx.el.p(
                    DocumentState.stats_processing,
                    class_name="text-3xl font-bold text-blue-600 mt-2",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3("Indexed", class_name="text-sm font-medium text-gray-500"),
                rx.el.p(
                    DocumentState.stats_completed,
                    class_name="text-3xl font-bold text-green-600 mt-2",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Quick Actions", class_name="text-lg font-semibold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("upload", class_name="h-6 w-6 mb-2 text-indigo-600"),
                    "Upload New",
                    on_click=lambda: DocumentState.set_view("upload"),
                    class_name="flex flex-col items-center justify-center p-6 bg-indigo-50 rounded-xl border border-indigo-100 hover:bg-indigo-100 transition-colors text-indigo-900 font-medium",
                ),
                rx.el.button(
                    rx.icon("search", class_name="h-6 w-6 mb-2 text-purple-600"),
                    "Search Library",
                    on_click=lambda: DocumentState.set_view("library"),
                    class_name="flex flex-col items-center justify-center p-6 bg-purple-50 rounded-xl border border-purple-100 hover:bg-purple-100 transition-colors text-purple-900 font-medium",
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-6",
            ),
            class_name="max-w-2xl w-full",
        ),
        class_name="p-4 md:p-8 w-full",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.match(
                    DocumentState.current_view,
                    ("dashboard", dashboard_widgets()),
                    ("library", library_view()),
                    ("upload", upload_area()),
                    ("detail", document_detail()),
                    ("search", search_view()),
                    (
                        "settings",
                        rx.el.div(
                            "Settings Not Implemented in Phase 1",
                            class_name="p-4 md:p-8 text-gray-500",
                        ),
                    ),
                    dashboard_widgets(),
                ),
                class_name="flex-1 overflow-y-auto bg-gray-50 w-full",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden relative",
        ),
        class_name="flex h-screen w-full bg-white font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/")