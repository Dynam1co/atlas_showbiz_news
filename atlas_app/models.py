"""All models in the database."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import datetime
from uuid import uuid4


class Item(Base):
    """Item object contains standar infrmation for a Movie or TV Show."""

    __tablename__ = 'item'

    id = Column(String, primary_key=True, index=True)
    media_type = Column(String)
    insert_datetime = Column(DateTime, default=datetime.datetime.now())
    insert_date = Column(Date, default=datetime.date.today())
    tmdb_id = Column(Integer, default=0)
    published_in_twitter = Column(Boolean, default=False)
    vote_average = Column(Float, default=0)
    poster_path = Column(String, default='')
    title = Column(String, default='')
    imdb_id = Column(String, default='')
    overview = Column(String, default='')
    time_window = Column(String)