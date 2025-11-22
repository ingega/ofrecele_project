import reflex as rx
from app.states.item_state import ItemState


def form_input(
    label: str,
    placeholder: str,
    value: rx.Var,
    on_change: rx.event.EventType,
    type_: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1.5"),
        rx.el.input(
            type=type_,
            placeholder=placeholder,
            on_change=on_change,
            class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 text-gray-800 placeholder-gray-400",
            default_value=value,
        ),
        class_name="mb-5",
    )


def form_textarea(
    label: str, placeholder: str, value: rx.Var, on_change: rx.event.EventType
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1.5"),
        rx.el.textarea(
            placeholder=placeholder,
            on_change=on_change,
            class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 text-gray-800 placeholder-gray-400 h-32 resize-none",
            default_value=value,
        ),
        class_name="mb-5",
    )


def item_card(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.cond(
                    item["image_url"] != "", item["image_url"], "/placeholder.svg"
                ),
                class_name="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500",
            ),
            class_name="h-48 w-full bg-gray-100 overflow-hidden relative",
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
                class_name="flex justify-between items-start mb-2",
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
                rx.el.a(
                    rx.el.button(
                        rx.icon("pencil", class_name="h-4 w-4"),
                        class_name="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                    ),
                    href=f"/dashboard/edit/{item['id']}",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=ItemState.open_delete_dialog(item["id"]),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                ),
                class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
            ),
            class_name="p-5",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200 group",
    )


def delete_confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 animate-in fade-in duration-200"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Delete Item", class_name="text-xl font-bold text-gray-900 mb-2"
                ),
                rx.radix.primitives.dialog.description(
                    "Are you sure you want to delete this item? This action cannot be undone.",
                    class_name="text-sm text-gray-500 mb-6",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            on_click=ItemState.close_delete_dialog,
                            class_name="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors",
                        )
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=ItemState.delete_item,
                        class_name="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg font-medium transition-colors shadow-sm",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-2xl p-6 w-[90vw] max-w-md z-50 animate-in fade-in zoom-in-95 duration-200",
            ),
        ),
        open=ItemState.show_delete_dialog,
        on_open_change=ItemState.close_delete_dialog,
    )