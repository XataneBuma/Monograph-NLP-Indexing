import reflex as rx
from app.states.document_state import DocumentState


def upload_area() -> rx.Component:
    upload_id = "monograph_upload"
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Upload Monographs",
                class_name="text-xl font-semibold text-gray-800 mb-2",
            ),
            rx.el.p(
                "Drag and drop PDF files here to start the indexing pipeline.",
                class_name="text-gray-500 mb-6",
            ),
            rx.upload.root(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "cloud-upload", class_name="h-16 w-16 text-indigo-400 mb-4"
                        ),
                        rx.el.p(
                            "Drag & Drop PDF files here",
                            class_name="text-lg font-medium text-gray-700",
                        ),
                        rx.el.p(
                            "or click to browse",
                            class_name="text-sm text-gray-500 mt-1",
                        ),
                        class_name="flex flex-col items-center justify-center z-10 relative",
                    ),
                    rx.el.div(
                        class_name="absolute inset-0 bg-indigo-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"
                    ),
                    class_name="relative flex flex-col items-center justify-center p-16 border-3 border-dashed border-indigo-200 rounded-2xl bg-white hover:border-indigo-400 transition-all duration-300 cursor-pointer group w-full",
                ),
                id=upload_id,
                accept={"application/pdf": [".pdf"]},
                multiple=True,
                max_files=10,
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Selected Files:",
                        class_name="text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.foreach(
                        rx.selected_files(upload_id),
                        lambda file: rx.el.div(
                            rx.icon("file-text", class_name="h-4 w-4 text-indigo-500"),
                            rx.el.span(
                                file, class_name="text-sm text-gray-600 truncate"
                            ),
                            class_name="flex items-center gap-2 p-2 bg-white border border-gray-200 rounded-lg shadow-sm",
                        ),
                    ),
                    class_name="flex flex-col gap-2",
                ),
                class_name="mt-6 p-4 bg-gray-50 rounded-xl border border-gray-200 min-h-[100px]",
            ),
            rx.el.div(
                rx.el.button(
                    "Clear Selection",
                    on_click=rx.clear_selected_files(upload_id),
                    class_name="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors",
                ),
                rx.el.button(
                    rx.cond(
                        DocumentState.is_uploading,
                        rx.el.span(
                            "Uploading...", class_name="flex items-center gap-2"
                        ),
                        rx.el.span(
                            "Start Upload & Processing",
                            class_name="flex items-center gap-2",
                        ),
                    ),
                    on_click=DocumentState.handle_upload(
                        rx.upload_files(upload_id=upload_id)
                    ),
                    disabled=DocumentState.is_uploading,
                    class_name="px-6 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed ml-auto",
                ),
                class_name="flex items-center gap-3 mt-6",
            ),
            class_name="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 max-w-3xl mx-auto",
        ),
        class_name="p-4 md:p-8 w-full",
    )