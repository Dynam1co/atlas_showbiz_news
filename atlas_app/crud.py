"""All API methods."""

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.sqltypes import Date, Integer
from . import models, schemas
import uuid
from uuid import uuid4


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