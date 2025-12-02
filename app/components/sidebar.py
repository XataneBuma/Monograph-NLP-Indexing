import reflex as rx
from app.states.document_state import DocumentState


def sidebar_item(icon: str, label: str, view_name: str) -> rx.Component:
    is_active = DocumentState.current_view == view_name
    return rx.el.button(
        rx.icon(
            icon,
            class_name=rx.cond(is_active, "text-white", "text-indigo-100"),
            size=20,
        ),
        rx.el.span(label, class_name="font-medium"),
        on_click=lambda: DocumentState.set_view(view_name),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-4 py-3 w-full rounded-xl bg-white/10 text-white transition-all duration-200",
            "flex items-center gap-3 px-4 py-3 w-full rounded-xl text-indigo-100 hover:bg-white/5 hover:text-white transition-all duration-200",
        ),
    )


def sidebar() -> rx.Component:
    return rx.fragment(
        rx.cond(
            DocumentState.is_sidebar_open,
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 z-40 md:hidden",
                on_click=DocumentState.close_sidebar,
            ),
            rx.fragment(),
        ),
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.icon("library", class_name="text-white h-8 w-8"),
                    rx.el.h1(
                        "UEM Monograph", class_name="text-xl font-bold text-white"
                    ),
                    class_name="flex items-center gap-3 px-4 py-6 mb-6 border-b border-indigo-500/30",
                ),
                rx.el.nav(
                    rx.el.div(
                        rx.el.p(
                            "MAIN MENU",
                            class_name="px-4 text-xs font-semibold text-indigo-300 mb-2 mt-2",
                        ),
                        sidebar_item("layout-dashboard", "Dashboard", "dashboard"),
                        sidebar_item("files", "Library", "library"),
                        sidebar_item("upload", "Upload", "upload"),
                        class_name="flex flex-col gap-1",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "TOOLS",
                            class_name="px-4 text-xs font-semibold text-indigo-300 mb-2 mt-6",
                        ),
                        sidebar_item("search", "Semantic Search", "search"),
                        sidebar_item("settings", "Settings", "settings"),
                        class_name="flex flex-col gap-1",
                    ),
                    class_name="flex flex-col gap-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("user_pen", class_name="h-8 w-8 text-indigo-200"),
                            rx.el.div(
                                rx.el.p(
                                    "Academic Admin",
                                    class_name="text-sm font-medium text-white",
                                ),
                                rx.el.p(
                                    "admin@uem.edu",
                                    class_name="text-xs text-indigo-200",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        class_name="mt-auto pt-6 border-t border-indigo-500/30 px-4 pb-6",
                    ),
                    class_name="mt-auto",
                ),
                class_name="flex flex-col h-full",
            ),
            class_name=rx.cond(
                DocumentState.is_sidebar_open, "translate-x-0", "-translate-x-full"
            )
            + " fixed inset-y-0 left-0 z-50 w-64 bg-indigo-900 transition-transform duration-300 ease-in-out md:translate-x-0 md:static md:inset-auto flex flex-col h-full shrink-0",
        ),
    )