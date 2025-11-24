#/app/models/models.py
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field

class AuctionItem(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    price: float
    image_url: str = Field(nullable=False)
    category: str = Field(nullable=False)
    owner: str = Field(index=True, nullable=False)
    active: bool = Field(nullable=False, default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserDB(SQLModel, table=True):
    # primary key
    id: Optional[int] = Field(primary_key=True, nullable=False, default=None)

    # user data fields
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)

    # security fields
    salt: str = Field(nullable=False)
    h_password: str = Field(nullable=False)  # h for hashed

    # rol fields
    is_active: bool = Field(nullable=False, default=True)
    is_superuser: bool = Field(nullable=False, default=False)
    is_staff: bool = Field(nullable=False, default=False)

    # creation/updating fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
