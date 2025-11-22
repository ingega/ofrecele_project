import reflex as rx
from app.states.auth_state import AuthState
from app.states.item_state import GLOBAL_ITEMS
import uuid
import datetime
import logging

GLOBAL_OFFERS: dict[str, dict] = {}


class OfferState(rx.State):
    """State for managing offers and bidding."""

    offer_amount: str = ""
    counter_amount: str = ""

    @rx.var
    async def my_incoming_offers(self) -> list[dict]:
        """Get offers received on my items."""
        auth_state = await self.get_state(AuthState)
        current_user = auth_state.current_username
        offers = []
        for offer in GLOBAL_OFFERS.values():
            if offer["seller_username"] == current_user:
                item = GLOBAL_ITEMS.get(offer["item_id"], {})
                offer_copy = offer.copy()
                offer_copy["item_title"] = item.get("title", "Unknown Item")
                offer_copy["item_image"] = item.get("image_url", "")
                offers.append(offer_copy)
        return sorted(offers, key=lambda x: x["created_at"], reverse=True)

    @rx.var
    async def my_outgoing_offers(self) -> list[dict]:
        """Get offers I have made."""
        auth_state = await self.get_state(AuthState)
        current_user = auth_state.current_username
        offers = []
        for offer in GLOBAL_OFFERS.values():
            if offer["buyer_username"] == current_user:
                item = GLOBAL_ITEMS.get(offer["item_id"], {})
                offer_copy = offer.copy()
                offer_copy["item_title"] = item.get("title", "Unknown Item")
                offer_copy["item_image"] = item.get("image_url", "")
                offers.append(offer_copy)
        return sorted(offers, key=lambda x: x["created_at"], reverse=True)

    @rx.var
    async def unread_offer_count(self) -> int:
        """Count of pending offers received."""
        auth_state = await self.get_state(AuthState)
        current_user = auth_state.current_username
        return len(
            [
                o
                for o in GLOBAL_OFFERS.values()
                if o["seller_username"] == current_user and o["status"] == "pending"
            ]
        )

    @rx.event
    def set_offer_amount(self, value: str):
        self.offer_amount = value

    @rx.event
    def set_counter_amount(self, value: str):
        self.counter_amount = value

    @rx.event
    async def submit_offer(self, item_id: str):
        """Submit a new offer for an item."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return rx.redirect("/login")
        if not self.offer_amount:
            return rx.toast("Please enter an offer amount")
        try:
            amount = float(self.offer_amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast("Invalid offer amount")
        item = GLOBAL_ITEMS.get(item_id)
        if not item:
            return rx.toast("Item not found")
        if item["owner"] == auth_state.current_username:
            return rx.toast("You cannot bid on your own item")
        existing_offer_id = None
        for oid, offer in GLOBAL_OFFERS.items():
            if (
                offer["item_id"] == item_id
                and offer["buyer_username"] == auth_state.current_username
                and (offer["status"] not in ["rejected", "accepted"])
            ):
                existing_offer_id = oid
                break
        offer_id = existing_offer_id if existing_offer_id else str(uuid.uuid4())
        offer_data = {
            "id": offer_id,
            "item_id": item_id,
            "buyer_username": auth_state.current_username,
            "seller_username": item["owner"],
            "offer_amount": str(amount),
            "status": "pending",
            "counter_offer_amount": "",
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now()),
        }
        GLOBAL_OFFERS[offer_id] = offer_data
        self.offer_amount = ""
        return rx.toast("Offer submitted successfully!")

    @rx.event
    async def accept_offer(self, offer_id: str):
        """Accept an incoming offer."""
        if offer_id in GLOBAL_OFFERS:
            GLOBAL_OFFERS[offer_id]["status"] = "accepted"
            GLOBAL_OFFERS[offer_id]["updated_at"] = str(datetime.datetime.now())
            return rx.toast("Offer accepted!")

    @rx.event
    async def reject_offer(self, offer_id: str):
        """Reject an incoming offer."""
        if offer_id in GLOBAL_OFFERS:
            GLOBAL_OFFERS[offer_id]["status"] = "rejected"
            GLOBAL_OFFERS[offer_id]["updated_at"] = str(datetime.datetime.now())
            return rx.toast("Offer rejected.")

    @rx.event
    async def counter_offer(self, offer_id: str):
        """Make a counter offer."""
        if not self.counter_amount:
            return rx.toast("Please enter a counter offer amount")
        if offer_id in GLOBAL_OFFERS:
            GLOBAL_OFFERS[offer_id]["counter_offer_amount"] = self.counter_amount
            GLOBAL_OFFERS[offer_id]["status"] = "countered"
            GLOBAL_OFFERS[offer_id]["updated_at"] = str(datetime.datetime.now())
            self.counter_amount = ""
            return rx.toast("Counter offer sent!")

    @rx.event
    async def cancel_offer(self, offer_id: str):
        """Cancel my outgoing offer."""
        if offer_id in GLOBAL_OFFERS:
            del GLOBAL_OFFERS[offer_id]
            return rx.toast("Offer cancelled.")