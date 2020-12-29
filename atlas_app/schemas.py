"""Pydantic models.

Define attributes to do API request.
"""

from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """Common attributes while creating o reading data."""

    email: str


class UserCreate(UserBase):
    """Common attributes while creating o reading data."""

    password: str


class User(UserBase):
    """Used when reading data, when returning it from the API."""

    id: int
    is_active: bool

    class Config:
        """Tell the Pydantic model to read the data even if it is not a dict."""

        orm_mode = True