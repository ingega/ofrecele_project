import reflex as rx
from app.states.offer_state import OfferState


def sidebar_item(
    text: str, icon: str, href: str, active: bool = False, badge: int = 0
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    icon,
                    class_name=f"h-5 w-5 {rx.cond(active, 'text-blue-600', 'text-gray-500')}",
                ),
                rx.el.span(
                    text,
                    class_name=f"font-medium {rx.cond(active, 'text-blue-700', 'text-gray-600')}",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.cond(
                badge > 0,
                rx.el.span(
                    badge,
                    class_name="bg-blue-600 text-white text-xs font-bold px-2 py-0.5 rounded-full",
                ),
            ),
            class_name=f"flex items-center justify-between px-3 py-2 rounded-lg transition-all duration-200 {rx.cond(active, 'bg-blue-50', 'hover:bg-gray-50')}",
        ),
        href=href,
        class_name="w-full",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "DASHBOARD",
                    class_name="text-xs font-bold text-gray-400 tracking-wider mb-4 block px-3",
                ),
                rx.el.nav(
                    sidebar_item("My Items", "package", "/dashboard"),
                    sidebar_item("Create Item", "circle_plus", "/dashboard/create"),
                    sidebar_item(
                        "My Offers",
                        "gavel",
                        "/dashboard/offers",
                        badge=OfferState.unread_offer_count,
                    ),
                    class_name="flex flex-col gap-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.span(
                    "MARKETPLACE",
                    class_name="text-xs font-bold text-gray-400 tracking-wider mb-4 block px-3",
                ),
                rx.el.nav(
                    sidebar_item("Browse Market", "shopping-bag", "/marketplace"),
                    class_name="flex flex-col gap-1",
                ),
            ),
            class_name="py-6",
        ),
        class_name="w-64 hidden md:block bg-white border-r border-gray-100 h-[calc(100vh-64px)] sticky top-16 overflow-y-auto px-4",
    )