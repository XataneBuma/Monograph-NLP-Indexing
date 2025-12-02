import reflex as rx
from app.states.document_state import DocumentState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", size=24, class_name="text-gray-600"),
                on_click=DocumentState.toggle_sidebar,
                class_name="mr-4 md:hidden p-2 hover:bg-gray-100 rounded-lg",
            ),
            rx.el.h2(
                rx.match(
                    DocumentState.current_view,
                    ("dashboard", "Dashboard Overview"),
                    ("library", "Document Library"),
                    ("upload", "Upload Documents"),
                    ("detail", "Document Details"),
                    ("search", "Semantic Search"),
                    "Dashboard",
                ),
                class_name="text-2xl font-bold text-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "bell",
                        class_name="text-gray-500 hover:text-indigo-600 transition-colors",
                        size=20,
                    ),
                    class_name="p-2 rounded-full hover:bg-gray-100 cursor-pointer",
                ),
                rx.el.div(
                    rx.icon(
                        "circle_plus",
                        class_name="text-gray-500 hover:text-indigo-600 transition-colors",
                        size=20,
                    ),
                    class_name="p-2 rounded-full hover:bg-gray-100 cursor-pointer",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name="h-20 px-4 md:px-8 flex items-center bg-white border-b border-gray-200",
    )