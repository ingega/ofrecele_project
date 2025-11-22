import reflex as rx
from app.components.navbar import navbar
from app.states.item_state import ItemState
from app.states.auth_state import AuthState
from app.states.offer_state import OfferState


def bid_section(item: dict) -> rx.Component:
    return rx.cond(
        AuthState.current_username != item["owner"],
        rx.el.div(
            rx.el.h3(
                "Make an Offer", class_name="text-lg font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "$",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 font-medium",
                    ),
                    rx.el.input(
                        type="number",
                        placeholder="Enter amount",
                        on_change=OfferState.set_offer_amount,
                        class_name="w-full pl-8 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                        default_value=OfferState.offer_amount,
                    ),
                    class_name="relative mb-4",
                ),
                rx.el.button(
                    "Submit Offer",
                    on_click=OfferState.submit_offer(item["id"]),
                    class_name="w-full py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/30 active:scale-95",
                ),
                class_name="bg-gray-50 p-6 rounded-2xl border border-gray-100",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("check_check", class_name="h-5 w-5 text-green-600 mr-2"),
                rx.el.span(
                    "You own this item", class_name="font-medium text-green-700"
                ),
                class_name="flex items-center bg-green-50 p-4 rounded-xl border border-green-100",
            )
        ),
    )


def item_detail_page() -> rx.Component:
    item = ItemState.current_item
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.cond(
                item,
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=rx.cond(
                                item["image_url"] != "",
                                item["image_url"],
                                "/placeholder.svg",
                            ),
                            class_name="w-full h-full object-cover",
                        ),
                        class_name="w-full md:w-1/2 h-96 md:h-auto bg-gray-100 rounded-2xl overflow-hidden shadow-inner",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                item["category"],
                                class_name="inline-block px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-sm font-medium mb-4",
                            ),
                            rx.el.h1(
                                item["title"],
                                class_name="text-3xl md:text-4xl font-bold text-gray-900 mb-4",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Current Price",
                                    class_name="text-sm text-gray-500 font-medium block mb-1",
                                ),
                                rx.el.span(
                                    f"${item['price']}",
                                    class_name="text-3xl font-bold text-gray-900",
                                ),
                                class_name="mb-8",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "Description",
                                    class_name="text-lg font-bold text-gray-900 mb-2",
                                ),
                                rx.el.p(
                                    item["description"],
                                    class_name="text-gray-600 leading-relaxed mb-8",
                                ),
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Seller", class_name="text-sm text-gray-500"
                                    ),
                                    rx.el.span(
                                        item["owner"],
                                        class_name="font-medium text-gray-900",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name="p-4 bg-gray-50 rounded-xl mb-8",
                            ),
                            bid_section(item),
                        ),
                        class_name="w-full md:w-1/2 flex flex-col",
                    ),
                    class_name="flex flex-col md:flex-row gap-8 md:gap-16",
                ),
                rx.el.div(
                    "Item not found",
                    class_name="text-center text-gray-500 text-xl py-20",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-20",
        ),
        class_name="min-h-screen bg-white font-['Montserrat']",
    )