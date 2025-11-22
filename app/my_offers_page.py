import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import sidebar
from app.states.offer_state import OfferState


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "pending",
            rx.el.span(
                "Pending",
                class_name="px-2 py-1 rounded-full bg-yellow-100 text-yellow-700 text-xs font-bold",
            ),
        ),
        (
            "accepted",
            rx.el.span(
                "Accepted",
                class_name="px-2 py-1 rounded-full bg-green-100 text-green-700 text-xs font-bold",
            ),
        ),
        (
            "rejected",
            rx.el.span(
                "Rejected",
                class_name="px-2 py-1 rounded-full bg-red-100 text-red-700 text-xs font-bold",
            ),
        ),
        (
            "countered",
            rx.el.span(
                "Countered",
                class_name="px-2 py-1 rounded-full bg-purple-100 text-purple-700 text-xs font-bold",
            ),
        ),
        rx.el.span(
            status,
            class_name="px-2 py-1 rounded-full bg-gray-100 text-gray-700 text-xs font-bold",
        ),
    )


def incoming_offer_card(offer: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.cond(
                    offer["item_image"] != "", offer["item_image"], "/placeholder.svg"
                ),
                class_name="w-20 h-20 object-cover rounded-lg",
            ),
            rx.el.div(
                rx.el.h3(offer["item_title"], class_name="font-bold text-gray-900"),
                rx.el.p(
                    f"Offer from: {offer['buyer_username']}",
                    class_name="text-sm text-gray-500",
                ),
                rx.el.p(
                    f"Amount: ${offer['offer_amount']}",
                    class_name="font-semibold text-blue-600 mt-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                status_badge(offer["status"]),
                class_name="flex flex-col items-end gap-2",
            ),
            class_name="flex gap-4",
        ),
        rx.cond(
            offer["status"] == "pending",
            rx.el.div(
                rx.el.button(
                    "Accept",
                    on_click=OfferState.accept_offer(offer["id"]),
                    class_name="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors",
                ),
                rx.el.button(
                    "Reject",
                    on_click=OfferState.reject_offer(offer["id"]),
                    class_name="px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 transition-colors",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Counter Amount",
                        on_change=OfferState.set_counter_amount,
                        class_name="px-3 py-2 border border-gray-200 rounded-lg text-sm w-32 focus:ring-2 focus:ring-blue-500 outline-none",
                    ),
                    rx.el.button(
                        "Counter",
                        on_click=OfferState.counter_offer(offer["id"]),
                        class_name="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors",
                    ),
                    class_name="flex gap-2",
                ),
                class_name="flex flex-wrap gap-3 mt-4 pt-4 border-t border-gray-100 items-center",
            ),
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )


def outgoing_offer_card(offer: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.cond(
                    offer["item_image"] != "", offer["item_image"], "/placeholder.svg"
                ),
                class_name="w-20 h-20 object-cover rounded-lg",
            ),
            rx.el.div(
                rx.el.h3(offer["item_title"], class_name="font-bold text-gray-900"),
                rx.el.p(
                    f"Seller: {offer['seller_username']}",
                    class_name="text-sm text-gray-500",
                ),
                rx.el.div(
                    rx.el.span(
                        f"My Offer: ${offer['offer_amount']}",
                        class_name="font-semibold text-blue-600 mr-3",
                    ),
                    rx.cond(
                        offer["counter_offer_amount"] != "",
                        rx.el.span(
                            f"Counter: ${offer['counter_offer_amount']}",
                            class_name="font-semibold text-purple-600",
                        ),
                    ),
                    class_name="mt-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                status_badge(offer["status"]),
                rx.cond(
                    offer["status"] == "pending",
                    rx.el.button(
                        "Cancel",
                        on_click=OfferState.cancel_offer(offer["id"]),
                        class_name="text-xs text-red-600 hover:text-red-700 font-medium mt-2",
                    ),
                ),
                class_name="flex flex-col items-end",
            ),
            class_name="flex gap-4",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )


def my_offers_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "My Offers", class_name="text-2xl font-bold text-gray-900 mb-8"
                    ),
                    rx.el.div(
                        rx.tabs.root(
                            rx.tabs.list(
                                rx.tabs.trigger(
                                    "Received Offers",
                                    value="received",
                                    class_name="px-4 py-2 font-medium text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 transition-colors",
                                ),
                                rx.tabs.trigger(
                                    "Sent Offers",
                                    value="sent",
                                    class_name="px-4 py-2 font-medium text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 transition-colors",
                                ),
                                class_name="flex gap-4 border-b border-gray-200 mb-6",
                            ),
                            rx.tabs.content(
                                rx.cond(
                                    OfferState.my_incoming_offers.length() > 0,
                                    rx.el.div(
                                        rx.foreach(
                                            OfferState.my_incoming_offers,
                                            incoming_offer_card,
                                        ),
                                        class_name="space-y-4",
                                    ),
                                    rx.el.p(
                                        "No incoming offers.",
                                        class_name="text-gray-500 text-center py-8",
                                    ),
                                ),
                                value="received",
                            ),
                            rx.tabs.content(
                                rx.cond(
                                    OfferState.my_outgoing_offers.length() > 0,
                                    rx.el.div(
                                        rx.foreach(
                                            OfferState.my_outgoing_offers,
                                            outgoing_offer_card,
                                        ),
                                        class_name="space-y-4",
                                    ),
                                    rx.el.p(
                                        "No sent offers.",
                                        class_name="text-gray-500 text-center py-8",
                                    ),
                                ),
                                value="sent",
                            ),
                            default_value="received",
                        )
                    ),
                    class_name="max-w-4xl mx-auto",
                ),
                class_name="flex-1 p-6 overflow-y-auto bg-gray-50/50",
            ),
            class_name="flex pt-16 h-screen",
        ),
        class_name="min-h-screen bg-white font-['Montserrat']",
    )