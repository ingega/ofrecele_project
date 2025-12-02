import reflex as rx
from app.states.auth_state import AuthState
from app.states.item_state import ItemState
from app.login_page import login_page
from app.register_page import register_page
from app.index_page import index_page
from app.dashboard_page import dashboard_page
from app.create_item_page import create_item_page
from app.edit_item_page import edit_item_page
from app.item_detail_page import item_detail_page
from app.marketplace_page import marketplace_page
from app.my_offers_page import my_offers_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index_page, route="/", title="Ofrecele Crypto | Home")
app.add_page(
    login_page,
    route="/login",
    title="Login | Ofrecele Crypto",
    on_load=AuthState.redirect_if_authenticated,
)
app.add_page(
    register_page,
    route="/register",
    title="Registro | ofrecele Crypto",
    on_load=AuthState.redirect_if_authenticated,
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    title="Dashboard | Offer Me Crypto",
    on_load=AuthState.check_auth,
)
app.add_page(
    create_item_page,
    route="/dashboard/create",
    title="Create Item | Offer Me Crypto",
    on_load=AuthState.check_auth,
)
app.add_page(
    edit_item_page,
    route="/dashboard/edit/[item_id]",
    title="Edit Item | Offer Me Crypto",
    on_load=[AuthState.check_auth, ItemState.load_item_for_edit],
)
app.add_page(
    item_detail_page, route="/items/[item_id]", title="Item Details | Offer Me Crypto"
)
app.add_page(
    marketplace_page, route="/marketplace", title="Marketplace | ofrecele Crypto"
)
app.add_page(
    my_offers_page,
    route="/dashboard/offers",
    title="dashboard | Offer Me Crypto",
    on_load=AuthState.check_auth,
)