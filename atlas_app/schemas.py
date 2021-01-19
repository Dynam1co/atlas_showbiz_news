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
    imdb_id: Optional[str] = ''
    title: Optional[str] = ''
    overview: Optional[str] = ''


class ItemUpdate(BaseModel):
    """Used when update item."""
    
    published_in_twitter: Optional[bool] = False
    imdb_id: Optional[str] = ''
    title: Optional[str] = ''
    overview: Optional[str] = ''


class Item(ItemBase):
    """Used when reading data, when returning it from the API."""

    insert_datetime: datetime
    insert_date: date
    published_in_twitter: bool    
    #imdb_id: Optional[str] = ''
    #title: Optional[str] = ''
    #overview: Optional[str] = ''

    class Config:
        """Tell the Pydantic model to read the data even if it is not a dict."""

        orm_mode = True


class TokenBase(BaseModel):
    """Common attributes while creating o reading data."""

    # id: str
    access_token: str
    refresh: str


class Token(TokenBase):
    """Used when reading data, when returning it from the API."""

    id: str
    insert_datetime: datetime

    class Config:
        """Tell the Pydantic model to read the data even if it is not a dict."""

        orm_mode = True


class BloggerPostBase(BaseModel):
    """Common attributes while creating o reading data."""

    id: str
    published_datetime: datetime
    updated_datetime: datetime
    post_url: str
    blog_id: str
    title: str
    content: str
    image_url: str
    labels: str


class BloggerPost(BloggerPostBase):
    """Used when reading data, when returning it from the API."""

    class Config:
        """Tell the Pydantic model to read the data even if it is not a dict."""

        orm_mode = True


class BloggerItemBase(BaseModel):
    """Common attributes while creating o reading data."""
        
    media_type: str = ''
    tmdb_id: str = ''
    vote_average: Optional[float] = 0
    poster_path: Optional[str] = ''
    title: str = ''
    imdb_id: Optional[str] = ''
    overview: Optional[str] = ''
    labels: List[str] = []


class BloggerItemUpdate(BaseModel):
    """Used when update item."""
    
    imdb_id: Optional[str] = ''
    overview: Optional[str] = ''
    vote_average: Optional[float] = 0    
    post_url: Optional[str] = ''
    blog_id: Optional[str] = ''


class BloggerItem(BloggerItemBase):
    """Used when reading data, when returning it from the API."""

    post_url: str
    blog_id: str
    id: str
    insert_datetime: datetime

    class Config:
        """Tell the Pydantic model to read the data even if it is not a dict."""

        orm_mode = True