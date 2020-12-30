"""Pydantic models.

Define attributes to do API request.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date


class ItemBase(BaseModel):
    """Common attributes while creating o reading data."""

    id: str
    media_type: str    
    tmdb_id: int    
    vote_average: Optional[float] = 0
    poster_path: Optional[str] = ''
    time_window: str


class Item(ItemBase):
    """Used when reading data, when returning it from the API."""

    insert_datetime: datetime
    insert_date: date
    published_in_twitter: bool    
    imdb_id: Optional[str] = ''
    title: Optional[str] = ''
    overview: Optional[str] = ''

    class Config:
        """Tell the Pydantic model to read the data even if it is not a dict."""

        orm_mode = True