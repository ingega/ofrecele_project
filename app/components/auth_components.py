import reflex as rx
from app.states.auth_state import AuthState


def form_field(
    label: str,
    placeholder: str,
    type_: str,
    on_change: rx.event.EventType,
    value: str = None,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            placeholder=placeholder,
            on_change=on_change,
            class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 text-gray-800 placeholder-gray-400",
            default_value=value,
        ),
        class_name="mb-4",
    )


def error_alert() -> rx.Component:
    return rx.cond(
        AuthState.error_message != "",
        rx.el.div(
            rx.icon("circle-alert", class_name="h-4 w-4 text-red-500 mr-2 shrink-0"),
            rx.el.span(AuthState.error_message, class_name="text-sm text-red-600"),
            class_name="flex items-center bg-red-50 border border-red-100 rounded-lg p-3 mb-6 animate-in fade-in slide-in-from-top-2 duration-300",
        ),
        rx.el.div(class_name="h-0"),
    )


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Bienvenido!", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p("Haz login y ofrecele!", class_name="text-gray-500 mt-2"),
            class_name="text-center mb-8",
        ),
        error_alert(),
        form_field(
            "Email", "you@example.com", "email", AuthState.set_login_email
        ),
        form_field("Password", "••••••••", "password", AuthState.set_login_password),
        rx.el.button(
            "login",
            on_click=AuthState.login,
            class_name="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5",
        ),
        rx.el.div(
            rx.el.span("Todavia no tienes cuenta? ", class_name="text-gray-500"),
            rx.el.a(
                "Crea una",
                href="/register",
                class_name="font-semibold text-blue-600 hover:text-blue-700 transition-colors",
            ),
            class_name="text-center mt-6 text-sm",
        ),
        class_name="bg-white p-8 sm:p-10 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md mx-auto",
    )


def register_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Create Account", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Comienza a ofrecer crypto por articulos", class_name="text-gray-500 mt-2"
            ),
            class_name="text-center mb-8",
        ),
        error_alert(),
        form_field("Usuario", "cryptoking", "text", AuthState.set_register_username),
        form_field(
            "Correo", "you@example.com", "email", AuthState.set_register_email
        ),
        form_field(
            "Password", "Min. 6 characters", "password", AuthState.set_register_password
        ),
        form_field(
            "Confirma Password",
            "Repite password",
            "password",
            AuthState.set_register_confirm_password,
        ),
        rx.el.button(
            "Crea cuenta",
            on_click=AuthState.register,
            class_name="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5",
        ),
        rx.el.div(
            rx.el.span("Ya tienes cuenta? ", class_name="text-gray-500"),
            rx.el.a(
                "Ingresa",
                href="/login",
                class_name="font-semibold text-blue-600 hover:text-blue-700 transition-colors",
            ),
            class_name="text-center mt-6 text-sm",
        ),
        class_name="bg-white p-8 sm:p-10 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md mx-auto",
    )