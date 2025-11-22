import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import sidebar
from app.components.item_components import item_card, delete_confirmation_dialog
from app.states.item_state import ItemState
from app.states.auth_state import AuthState


def dashboard_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "My Items", class_name="text-2xl font-bold text-gray-900"
                        ),
                        rx.el.a(
                            rx.el.button(
                                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                                "Create New",
                                class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm",
                            ),
                            href="/dashboard/create",
                        ),
                        class_name="flex justify-between items-center mb-8",
                    ),
                    rx.cond(
                        ItemState.my_items.length() > 0,
                        rx.el.div(
                            rx.foreach(ItemState.my_items, item_card),
                            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                        ),
                        rx.el.div(
                            rx.icon(
                                "package-open",
                                class_name="h-12 w-12 text-gray-300 mb-4",
                            ),
                            rx.el.h3(
                                "No items found",
                                class_name="text-lg font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "Get started by creating your first auction item.",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="flex flex-col items-center justify-center py-20 bg-white rounded-2xl border border-dashed border-gray-300",
                        ),
                    ),
                    delete_confirmation_dialog(),
                    class_name="max-w-7xl mx-auto",
                ),
                class_name="flex-1 p-6 overflow-y-auto bg-gray-50/50",
            ),
            class_name="flex pt-16 h-screen",
        ),
        class_name="min-h-screen bg-white font-['Montserrat']",
    )