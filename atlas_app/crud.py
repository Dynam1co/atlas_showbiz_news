"""All API methods."""

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.sqltypes import Date, Integer
from . import models, schemas
import uuid
from uuid import uuid4
from typing import Optional


def get_item(db: Session, item_id: str):
    """Return data for a single Item."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def update_item(db: Session, item: schemas.ItemUpdate, stored_item: schemas.Item):
    """Update a single Item."""
    if item.title != '':
        stored_item.title = item.title

    if item.imdb_id != '':
        stored_item.imdb_id = item.imdb_id 

    if item.published_in_twitter != stored_item.published_in_twitter:
        stored_item.published_in_twitter = item.published_in_twitter

    if item.overview != '':
        stored_item.overview = item.overview
    
    db.commit()
    db.refresh(stored_item)
    return stored_item


def get_items(db: Session):
    """Return data for all Items."""
    return db.query(models.Item).all()


def get_item_by_date(db: Session, dt_insert: Date):
    """Search items by insertion date."""
    return db.query(models.Item).filter(models.Item.insert_date == dt_insert).all()


def get_item_by_date_and_tmdbid(db: Session, dt_insert: Date, tmdb_id: Integer):
    """Search items by insertion date and tmdb id."""
    return db.query(models.Item).filter(
        models.Item.insert_date == dt_insert,
        models.Item.tmdb_id == tmdb_id
    ).first()


def create_item(db: Session, item: schemas.ItemBase):
    """Insert item into database."""
    db_item = models.Item(
        id=item.id,
        media_type=item.media_type,
        tmdb_id=item.tmdb_id,
        vote_average=item.vote_average,
        poster_path=item.poster_path,
        time_window=item.time_window,        
        title=item.title,
        imdb_id=item.imdb_id,
        overview=item.overview
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_token(db: Session, token: schemas.TokenBase):
    """Insert new token into database."""
    db_token = models.Token(
        access_token=token.access_token,
        refresh=token.refresh
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_last_token(db: Session):
    """Return last token from database."""
    return db.query(models.Token).order_by(desc(models.Token.insert_datetime)).first()


def create_blogger_post(db: Session, post: schemas.BloggerPostBase):
    """Insert new blogger post into database."""
    db_blogger_post = models.BloggerPost(
        id=post.id,
        published_datetime=post.published_datetime,
        updated_datetime=post.updated_datetime,
        post_url=post.post_url,
        blog_id=post.blog_id,
        title=post.title,
        content=post.content,
        image_url=post.image_url,
        labels=str(post.labels)
    )

    db.add(db_blogger_post)
    db.commit()
    db.refresh(db_blogger_post)
    return db_blogger_post


def get_blogger_posts(db: Session):
    """Return all bloger posts from de database."""
    return db.query(models.BloggerPost).all()


def create_blogger_item(db: Session, blogit: schemas.BloggerItemBase):
    """Insert new blogger item into database."""
    db_blogger_item = models.BloggerItem(
        media_type=blogit.media_type,
        tmdb_id=blogit.tmdb_id,
        vote_average=blogit.vote_average,
        poster_path=blogit.poster_path,
        title=blogit.title,
        imdb_id=blogit.imdb_id,
        overview=blogit.overview,
        labels=blogit.labels
    )

    db.add(db_blogger_item)
    db.commit()
    db.refresh(db_blogger_item)
    return db_blogger_item


def get_blogger_item(db: Session, item_id: str):
    """Return data for a single Item."""
    return db.query(models.BloggerItem).filter(models.BloggerItem.id == item_id).first()


def update_blogger_item(db: Session, blogit: schemas.BloggerItemUpdate, stored_item: schemas.BloggerItem):
    """Update a single Blogger Item."""
    if blogit.imdb_id != '':
        stored_item.imdb_id = blogit.imdb_id     

    if blogit.overview != '':
        stored_item.overview = blogit.overview

    if blogit.vote_average != 0:
        stored_item.vote_average = blogit.vote_average

    if blogit.post_url != '':
        stored_item.post_url = blogit.post_url

    if blogit.blog_id != '':
        stored_item.blog_id = blogit.blog_id
    
    db.commit()
    db.refresh(stored_item)
    return stored_item


def get_blogger_items(db: Session, tmdb_id: Optional[str] = None):
    """Return data for all Items."""
    if tmdb_id:
        return db.query(models.BloggerItem).filter(models.BloggerItem.tmdb_id == tmdb_id).all()

    return db.query(models.BloggerItem).all()