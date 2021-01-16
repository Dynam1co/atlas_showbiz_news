"""Integrate parts of FastAPI elements."""

from typing import List
from typing import Optional
import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Date

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():    
    """Create a new SQLAlchemy SessionLocal.

    That will be used in a single request,
    and then close it once the request is finished.
    """    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """Show base url."""
    return {"message": "Hello World"}


@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    """Create Item."""    
    db_item = crud.get_item_by_date_and_tmdbid(db, datetime.date.today(), item.tmdb_id)

    if db_item:
        raise HTTPException(status_code=400, detail="Item already registered")

    return crud.create_item(db=db, item=item)


@app.patch("/items/{item_id}", response_model=schemas.Item)
def update_item(updated_item: schemas.ItemUpdate, item_id: str, db: Session = Depends(get_db)):
    """Update Item."""
    db_item = crud.get_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return crud.update_item(db=db, item=updated_item, stored_item=db_item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db), item_type: Optional[str] = None, date_insert: Optional[str] = None, period: Optional[str] = None):
    """Read Items."""        
    results = crud.get_items(db)

    if item_type:
        results = [x for x in results if x.media_type == item_type]

    if date_insert:
        results = [x for x in results if x.insert_date == date_insert]

    if period:
        results = [x for x in results if x.time_window == period]

    return results


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: str, db: Session = Depends(get_db)):
    """Read single item."""
    db_item = crud.get_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item
