import reflex as rx
from app.components.navbar import navbar
from app.components.auth_components import login_form
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            login_form(),
            class_name="flex-1 flex items-center justify-center px-4 py-20 sm:px-6 lg:px-8",
        ),
        class_name="min-h-screen flex flex-col bg-gray-50/50 font-['Montserrat']",
    )