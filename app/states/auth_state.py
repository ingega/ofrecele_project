import reflex as rx
import hashlib
import os
import re

from sqlalchemy.testing.suite.test_reflection import users
from sqlmodel import select
from typing import Optional, List

from app.models.models import UserDB

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
        """Handle user login by querying the database and verifying the password."""
        if not self.login_email or not self.login_password:
            self.error_message = "Por favor llena todos los campos obligatorios."
            return

        # 1. Query the database for the user by email
        db_user: Optional[UserDB] = None
        with rx.session() as session:
            db_user = session.exec(
                select(UserDB).where(UserDB.email == self.login_email)
            ).first()

        # 2. Check if a user was found
        if not db_user:
            # Always return a generic error message for security
            self.error_message = "email o password incorrecto."
            return

        # 3. Retrieve stored salt and hash (must be converted back to bytes)
        # NOTE: UserDB model's salt and h_password are as strings
        try:
            stored_salt = db_user.salt.encode('utf-8')  # stored as hex string/text
            stored_hash = db_user.h_password.encode('utf-8')  # hex string/text
        except AttributeError:
            # If the fields are stored directly as bytes/BLOB, just use them:
            stored_salt = db_user.salt
            stored_hash = db_user.h_password

        # 4. Hash the input password using the stored salt
        input_hash, _ = self._hash_password(self.login_password, stored_salt)

        # 5. Compare the input hash with the stored hash
        if input_hash == stored_hash:
            # Login Success
            self.is_authenticated = True
            self.current_username = db_user.username
            self.current_email = db_user.email
            self.error_message = ""
            self.login_password = ""
            return rx.redirect("/")
        else:
            # Password mismatch
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

        # add the salt and hash the password
        pwd_hash, salt = self._hash_password(self.register_password)
        # finally add tue user to db
        new_user = UserDB(
            username=self.register_username,
            email=self.register_email,
            salt=salt,
            h_password=pwd_hash
        )
        with rx.session() as session:
            session.add(new_user)
            session.commit()

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