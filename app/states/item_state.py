import uuid
import reflex as rx
from sqlmodel import select
from typing import List, Dict, Any
from app.states.auth_state import AuthState
from app.models.models import AuctionItem

GLOBAL_ITEMS: dict[str, dict[str, str]] = {}


class ItemState(rx.State):
    """State for managing auction items."""

    form_title: str = ""
    form_description: str = ""
    form_price: str = ""
    form_image_url: str = ""
    form_category: str = "Other"
    editing_item_id: str = ""
    show_delete_dialog: bool = False
    item_id_to_delete: str = ""
    categories: list[str] = ["NFTs", "Tokens", "Domain Names", "Other"]

    @rx.var
    async def my_items(self) -> List[Dict[str, Any]]:
        """Get items owned by the current user from the database."""
        # 1. Get the current username from the authentication state
        auth_state = await self.get_state(AuthState)
        username = auth_state.current_username

        if not username:
            return []

        # 2. Query the database for items matching the owner
        with rx.session() as session:
            db_items: List[AuctionItem] = session.exec(
                select(AuctionItem).where(AuctionItem.owner == username)
            ).all()

            # 3. Convert SQLModel objects to dictionaries for the frontend
            return [item.model_dump() for item in db_items]

    @rx.var
    def all_items(self) -> list[dict[str, str]]:
        """Get all items available in the marketplace."""
        with rx.session() as session:
            # Query the database for all active AuctionItem records
            db_items: List[AuctionItem] = session.exec(
                select(AuctionItem).where(AuctionItem.active == True)
            ).all()

            # Convert SQLModel objects to dictionaries for easier frontend display
            # We use .model_dump() (or .dict() depending on Pydantic version)
            return [item.model_dump() for item in db_items]

    @rx.var
    def current_item(self) -> Dict[str, Any]:
        """
        Get the item details for the current page params by querying the database.

        This method is triggered automatically when the /auctions/[item_id] route is accessed.
        """

        # 1. Get the dynamic parameter from the URL
        item_id = self.router.page.params.get("item_id")

        if not item_id:
            return {}  # Return empty if no ID is in the URL

        # 2. Query the database for the item with the matching ID
        with rx.session() as session:
            # Note: Assuming your AuctionItem.id is a string (UUID) based on your create_item
            item = session.exec(
                select(AuctionItem).where(AuctionItem.id == item_id)
            ).first()

            # 3. Check if the item exists and return it as a dictionary
            if item:
                # Use model_dump() (or .dict()) to convert the SQLModel object to a dictionary
                # that the frontend can easily read and render.
                return item.model_dump()
            else:
                # Return empty dictionary if item is not found in the DB
                return {}

    @rx.event
    def set_form_title(self, value: str):
        self.form_title = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_price(self, value: str):
        self.form_price = value

    @rx.event
    def set_form_image_url(self, value: str):
        self.form_image_url = value

    @rx.event
    def set_form_category(self, value: str):
        self.form_category = value

    def _reset_form(self):
        self.form_title = ""
        self.form_description = ""
        self.form_price = ""
        self.form_image_url = ""
        self.form_category = "Other"
        self.editing_item_id = ""

    @rx.event
    async def create_item(self):
        """Create a new item."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return rx.redirect("/login")
        if not self.form_title or not self.form_price:
            return rx.toast.error("Title and Price are required.")
        item_id = str(uuid.uuid4())
        new_item = AuctionItem(
            id=item_id,
            owner=auth_state.current_username,
            title=self.form_title,
            description=self.form_description,
            price=self.form_price,
            image_url=self.form_image_url,
            category=self.form_category,
        )
        with rx.session() as session:
            session.add(new_item)
            session.commit()

        # once added the Item, restart the form
        self._reset_form()
        return rx.redirect("/dashboard")

    @rx.event
    def load_item_for_edit(self):
        """Load item data into form for editing."""
        item_id = self.router.page.params.get("item_id")
        if item_id in GLOBAL_ITEMS:
            item = GLOBAL_ITEMS[item_id]
            self.editing_item_id = item_id
            self.form_title = item["title"]
            self.form_description = item["description"]
            self.form_price = item["price"]
            self.form_image_url = item["image_url"]
            self.form_category = item["category"]

    @rx.event
    async def update_item(self):
        """Update an existing item."""
        if not self.editing_item_id or self.editing_item_id not in GLOBAL_ITEMS:
            return rx.toast.error("Item not found.")
        auth_state = await self.get_state(AuthState)
        item = GLOBAL_ITEMS[self.editing_item_id]
        if item["owner"] != auth_state.current_username:
            return rx.toast.error("You do not own this item.")
        GLOBAL_ITEMS[self.editing_item_id].update(
            {
                "title": self.form_title,
                "description": self.form_description,
                "price": self.form_price,
                "image_url": self.form_image_url,
                "category": self.form_category,
            }
        )
        self._reset_form()
        return rx.redirect("/dashboard")

    @rx.event
    def open_delete_dialog(self, item_id: str):
        self.item_id_to_delete = item_id
        self.show_delete_dialog = True

    @rx.event
    def close_delete_dialog(self):
        self.show_delete_dialog = False
        self.item_id_to_delete = ""

    @rx.event
    async def delete_item(self):
        """Delete the selected item."""
        if not self.item_id_to_delete or self.item_id_to_delete not in GLOBAL_ITEMS:
            self.close_delete_dialog()
            return
        auth_state = await self.get_state(AuthState)
        item = GLOBAL_ITEMS[self.item_id_to_delete]
        if item["owner"] == auth_state.current_username:
            del GLOBAL_ITEMS[self.item_id_to_delete]
        self.close_delete_dialog()