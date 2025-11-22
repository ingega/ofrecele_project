import reflex as rx
from app.states.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("coins", class_name="h-8 w-8 text-blue-600"),
                    rx.el.span(
                        "Offer Me Crypto",
                        class_name="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 text-transparent bg-clip-text",
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.span(
                            f"Hello, {AuthState.current_username}",
                            class_name="text-gray-600 font-medium hidden sm:block",
                        ),
                        rx.el.a(
                            "Marketplace",
                            href="/marketplace",
                            class_name="text-gray-600 font-medium hover:text-blue-600 transition-colors mr-2",
                        ),
                        rx.el.button(
                            rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                            "Sign Out",
                            on_click=AuthState.logout,
                            class_name="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Log In",
                            href="/login",
                            class_name="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors",
                        ),
                        rx.el.a(
                            "Get Started",
                            href="/register",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between",
        ),
        class_name="bg-white/80 backdrop-blur-md border-b border-gray-100 fixed w-full top-0 z-50",
    )