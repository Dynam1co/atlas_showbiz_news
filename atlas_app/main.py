"""Integrate parts of FastAPI elements."""

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

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
    return crud.create_item(db=db, item=item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    """Read Items."""
    return crud.get_items(db)


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: str, db: Session = Depends(get_db)):
    """Read single item."""
    db_item = crud.get_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item