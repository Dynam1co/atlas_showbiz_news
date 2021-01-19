"""All models in the database."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import datetime
import uuid
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

class Token(Base):
    """Token contains info for publish in Blogger."""

    __tablename__ = 'blogger_token'

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid1()))
    insert_datetime = Column(DateTime, default=datetime.datetime.now())
    access_token = Column(String)
    refresh = Column(String)


class BloggerPost(Base):
    """Google Blogger post."""

    __tablename__ = 'blogger_post'

    id = Column(String, primary_key=True, index=True)
    published_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)
    post_url = Column(String, default='')
    blog_id = Column(String, default='')
    title = Column(String, default='')
    content = Column(String, default='')
    image_url = Column(String, default='')
    labels = Column(String, default='')


class BloggerItem(Base):
    """Google Blogger Item."""

    __tablename__ = 'blogger_item'

    # id = Column(String, primary_key=True, index=True, default=str(uuid.uuid1()))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    insert_datetime = Column(DateTime, default=datetime.datetime.now())
    media_type = Column(String)
    tmdb_id = Column(Integer, default=0)
    vote_average = Column(Float, default=0)
    poster_path = Column(String, default='')
    title = Column(String, default='')
    imdb_id = Column(String, default='')
    overview = Column(String, default='')
    post_url = Column(String, default='')
    blog_id = Column(String, default='')
    labels = Column(String, default='')