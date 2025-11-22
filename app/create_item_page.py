import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import sidebar
from app.components.item_components import form_input, form_textarea
from app.states.item_state import ItemState


def create_item_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Create New Item",
                        class_name="text-2xl font-bold text-gray-900 mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            form_input(
                                "Item Title",
                                "e.g. Bored Ape #1234",
                                ItemState.form_title,
                                ItemState.set_form_title,
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Category",
                                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                                ),
                                rx.el.select(
                                    rx.foreach(
                                        ItemState.categories,
                                        lambda x: rx.el.option(x, value=x),
                                    ),
                                    value=ItemState.form_category,
                                    on_change=ItemState.set_form_category,
                                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 text-gray-800 appearance-none cursor-pointer",
                                ),
                                class_name="mb-5",
                            ),
                            rx.el.div(
                                form_input(
                                    "Starting Price ($)",
                                    "0.00",
                                    ItemState.form_price,
                                    ItemState.set_form_price,
                                ),
                                class_name="w-full",
                            ),
                            form_input(
                                "Image URL",
                                "https://...",
                                ItemState.form_image_url,
                                ItemState.set_form_image_url,
                            ),
                            form_textarea(
                                "Description",
                                "Describe your item...",
                                ItemState.form_description,
                                ItemState.set_form_description,
                            ),
                            rx.el.div(
                                rx.el.a(
                                    "Cancel",
                                    href="/dashboard",
                                    class_name="px-6 py-2.5 text-gray-700 font-medium hover:bg-gray-100 rounded-lg transition-colors",
                                ),
                                rx.el.button(
                                    "Create Item",
                                    on_click=ItemState.create_item,
                                    class_name="px-6 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md",
                                ),
                                class_name="flex justify-end gap-4 mt-8 items-center",
                            ),
                            class_name="space-y-1",
                        ),
                        class_name="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-2xl",
                    ),
                    class_name="max-w-7xl mx-auto",
                ),
                class_name="flex-1 p-6 overflow-y-auto bg-gray-50/50",
            ),
            class_name="flex pt-16 h-screen",
        ),
        class_name="min-h-screen bg-white font-['Montserrat']",
    )