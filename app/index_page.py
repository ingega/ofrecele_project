from wsgiref.validate import header_re

import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState


def index_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.el.div(
                            rx.el.span(
                                "Bienvenido!",
                                class_name="inline-block py-1 px-3 rounded-full bg-blue-100 text-blue-700 text-sm font-semibold mb-6",
                            ),
                            rx.el.h1(
                                rx.el.span("Listo para ", class_name="block"),
                                rx.el.span("Ofrecer?", class_name="text-blue-600"),
                                class_name="text-4xl md:text-6xl font-bold text-gray-900 tracking-tight mb-6 leading-tight",
                            ),
                            rx.el.p(
                                "Tu panel esta listo. Encuentra el articulo que estas buscando.",
                                class_name="text-xl text-gray-600 mb-10 max-w-2xl mx-auto",
                            ),
                            rx.el.div(
                                rx.el.a(
                                    rx.el.button(
                                        "Navega por los items",
                                        rx.icon(
                                            "arrow-right", class_name="ml-2 w-5 h-5"
                                        ),
                                        class_name="flex items-center px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/30 hover:-translate-y-1",
                                    ),
                                    href="/marketplace",
                                ),
                                rx.el.a(
                                    rx.el.button(
                                        "Agrega un articulo!",
                                        rx.icon(
                                            "arrow-right", class_name="ml-2 w-5 h-5"
                                        ),
                                        class_name="flex items-center px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/30 hover:-translate-y-1",
                                    ),
                                    href="/dashboard/create",
                                ),
                                class_name="flex gap-4 justify-center",
                            ),
                            class_name="text-center",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h1(
                                    "El mercado Premier para",
                                    rx.el.br(),
                                    rx.el.span(
                                        "Cryptonautas",
                                        class_name="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600",
                                    ),
                                    class_name="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight mb-8 leading-tight",
                                ),
                                rx.el.p(
                                    "Ofrecele es seguro, regatea en tiempo real con usuarios verificados. "
                                    "Unete al mercado desentralizado del futuro.",
                                    class_name="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed",
                                ),
                                rx.el.div(
                                    rx.el.a(
                                        rx.el.button(
                                            "Comienza a ofrecer ya!",
                                            rx.icon(
                                                "arrow-right", class_name="ml-2 w-5 h-5"
                                            ),
                                            class_name="flex items-center px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/30 hover:-translate-y-1",
                                        ),
                                        href="/register",
                                    ),
                                    rx.el.a(
                                        rx.el.button(
                                            "Modo Demo",
                                            class_name="px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-xl font-semibold hover:bg-gray-50 transition-all hover:-translate-y-1",
                                        ),
                                        href="/login",
                                    ),
                                    class_name="flex flex-col sm:flex-row gap-4 justify-center items-center",
                                ),
                                class_name="text-center",
                            )
                        ),
                    ),
                    class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20",
                ),
                class_name="bg-gradient-to-b from-blue-50/50 via-white to-white w-full",
            ),
            class_name="flex-1 w-full",
        ),
        class_name="min-h-screen flex flex-col bg-white font-['Montserrat']",
    )