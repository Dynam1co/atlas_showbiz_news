"""All API methods."""

from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Date
from . import models, schemas


def get_item(db: Session, item_id: str):
    """Return data for a single Item."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session):
    """Return data for all Items."""
    return db.query(models.Item).all()


def get_item_by_date(db: Session, dt_insert: Date):
    """Search items by insertion date."""
    return db.query(models.Item).filter(models.Item.insert_date == dt_insert).all()


def create_item(db: Session, item: schemas.ItemBase):
    """Insert item into database."""
    db_item = models.Item(
        id=item.id,
        media_type=item.media_type,
        tmdb_id=item.tmdb_id,
        vote_average=item.vote_average,
        poster_path=item.poster_path,
        time_window=item.time_window
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item