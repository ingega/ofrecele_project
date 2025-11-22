import reflex as rx
from app.components.navbar import navbar
from app.states.item_state import ItemState


def marketplace_item_card(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.cond(
                    item["image_url"] != "", item["image_url"], "/placeholder.svg"
                ),
                class_name="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500",
            ),
            class_name="h-56 w-full bg-gray-100 overflow-hidden relative",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    item["category"],
                    class_name="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full",
                ),
                rx.el.span(
                    f"${item['price']}", class_name="text-lg font-bold text-gray-900"
                ),
                class_name="flex justify-between items-start mb-3",
            ),
            rx.el.h3(
                item["title"],
                class_name="text-lg font-bold text-gray-900 mb-1 truncate",
            ),
            rx.el.p(
                item["description"],
                class_name="text-sm text-gray-500 line-clamp-2 mb-4 h-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Seller:", class_name="text-xs text-gray-400 mr-1"),
                    rx.el.span(
                        item["owner"], class_name="text-xs font-medium text-gray-600"
                    ),
                    class_name="flex items-center",
                ),
                rx.el.a(
                    rx.el.button(
                        "View Item",
                        class_name="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors shadow-sm",
                    ),
                    href=f"/items/{item['id']}",
                ),
                class_name="flex justify-between items-center pt-4 border-t border-gray-100",
            ),
            class_name="p-5",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200 group",
    )


def marketplace_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Marketplace", class_name="text-3xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Discover unique crypto assets and collectibles",
                        class_name="text-gray-500 mt-2",
                    ),
                    class_name="mb-8",
                ),
                rx.cond(
                    ItemState.all_items.length() > 0,
                    rx.el.div(
                        rx.foreach(ItemState.all_items, marketplace_item_card),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8",
                    ),
                    rx.el.div(
                        rx.icon(
                            "shopping-bag", class_name="h-16 w-16 text-gray-300 mb-4"
                        ),
                        rx.el.h3(
                            "Marketplace is empty",
                            class_name="text-xl font-medium text-gray-900",
                        ),
                        rx.el.p(
                            "Be the first to list an item for auction.",
                            class_name="text-gray-500 mt-2",
                        ),
                        class_name="flex flex-col items-center justify-center py-32 bg-white rounded-2xl border border-dashed border-gray-300",
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
            ),
            class_name="bg-gray-50/50 min-h-screen",
        ),
        class_name="min-h-screen bg-white font-['Montserrat']",
    )