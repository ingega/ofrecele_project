import reflex as rx
import hashlib
import os
import re
from typing import Optional

GLOBAL_USERS = {}


class AuthState(rx.State):
    """State for user authentication and registration."""

    is_authenticated: bool = False
    current_username: str = ""
    current_email: str = ""
    login_email: str = ""
    login_password: str = ""
    register_email: str = ""
    register_username: str = ""
    register_password: str = ""
    register_confirm_password: str = ""
    error_message: str = ""

    def _validate_email(self, email: str) -> bool:
        """Simple email validation regex."""
        pattern = "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
        return bool(re.match(pattern, email))

    def _hash_password(
        self, password: str, salt: Optional[bytes] = None
    ) -> tuple[bytes, bytes]:
        """Hash a password using PBKDF2."""
        if salt is None:
            salt = os.urandom(32)
        pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return (pwd_hash, salt)

    @rx.event
    def set_login_email(self, value: str):
        self.login_email = value
        self.error_message = ""

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value
        self.error_message = ""

    @rx.event
    def set_register_email(self, value: str):
        self.register_email = value
        self.error_message = ""

    @rx.event
    def set_register_username(self, value: str):
        self.register_username = value
        self.error_message = ""

    @rx.event
    def set_register_password(self, value: str):
        self.register_password = value
        self.error_message = ""

    @rx.event
    def set_register_confirm_password(self, value: str):
        self.register_confirm_password = value
        self.error_message = ""

    @rx.event
    async def login(self):
        """Handle user login."""
        if not self.login_email or not self.login_password:
            self.error_message = "Please fill in all fields."
            return
        user_found = None
        found_username = None
        for username, data in GLOBAL_USERS.items():
            if data["email"] == self.login_email:
                user_found = data
                found_username = username
                break
        if not user_found:
            self.error_message = "Invalid email or password."
            return
        stored_hash = user_found["password_hash"]
        salt = user_found["salt"]
        input_hash, _ = self._hash_password(self.login_password, salt)
        if input_hash == stored_hash:
            self.is_authenticated = True
            self.current_username = found_username
            self.current_email = self.login_email
            self.error_message = ""
            self.login_password = ""
            return rx.redirect("/")
        else:
            self.error_message = "Invalid email or password."

    @rx.event
    async def register(self):
        """Handle new user registration."""
        if not all(
            [
                self.register_email,
                self.register_username,
                self.register_password,
                self.register_confirm_password,
            ]
        ):
            self.error_message = "All fields are required."
            return
        if not self._validate_email(self.register_email):
            self.error_message = "Invalid email address."
            return
        if len(self.register_password) < 6:
            self.error_message = "Password must be at least 6 characters long."
            return
        if self.register_password != self.register_confirm_password:
            self.error_message = "Passwords do not match."
            return
        if self.register_username in GLOBAL_USERS:
            self.error_message = "Username already taken."
            return
        for data in GLOBAL_USERS.values():
            if data["email"] == self.register_email:
                self.error_message = "Email already registered."
                return
        pwd_hash, salt = self._hash_password(self.register_password)
        GLOBAL_USERS[self.register_username] = {
            "email": self.register_email,
            "password_hash": pwd_hash,
            "salt": salt,
        }
        self.is_authenticated = True
        self.current_username = self.register_username
        self.current_email = self.register_email
        self.register_password = ""
        self.register_confirm_password = ""
        self.error_message = ""
        return rx.redirect("/")

    @rx.event
    def logout(self):
        """Log the user out."""
        self.is_authenticated = False
        self.current_username = ""
        self.current_email = ""
        return rx.redirect("/login")

    @rx.event
    def check_auth(self):
        """Redirect to login if not authenticated."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def redirect_if_authenticated(self):
        """Redirect to home if already authenticated."""
        if self.is_authenticated:
            return rx.redirect("/")