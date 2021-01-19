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
        print(f"Item: {item.title} already registered. {datetime.datetime.now()}")
        # raise HTTPException(status_code=400, detail="Item already registered")
        return db_item

    return crud.create_item(db=db, item=item)


@app.patch("/items/{item_id}", response_model=schemas.Item)
def update_item(updated_item: schemas.ItemUpdate, item_id: str, db: Session = Depends(get_db)):
    """Update Item."""
    db_item = crud.get_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return crud.update_item(db=db, item=updated_item, stored_item=db_item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db), item_type: Optional[str] = None, date_insert: Optional[datetime.date] = None, period: Optional[str] = None, twitter_published: Optional[bool] = None):
    """Read Items."""        
    results = crud.get_items(db)

    if item_type:
        results = [x for x in results if x.media_type == item_type]

    if date_insert:
        results = [x for x in results if x.insert_date == date_insert]    

    if period:
        results = [x for x in results if x.time_window == period]

    if twitter_published != None:
        results = [x for x in results if x.published_in_twitter == twitter_published]   

    return results


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: str, db: Session = Depends(get_db)):
    """Read single item."""
    db_item = crud.get_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@app.post("/tokens/", response_model=schemas.Token, summary='Create Token')
def create_token(token: schemas.TokenBase, db: Session = Depends(get_db)):
    """Create Token."""
    return crud.create_token(db=db, token=token)


@app.get("/tokens/", response_model=schemas.Token, summary='Get latest Token')
def read_tokens(db: Session = Depends(get_db)):
    """Read Items."""        
    return crud.get_last_token(db)    


@app.post("/blogger_posts/", response_model=schemas.BloggerPost, summary='Create Blogger post')
def create_blogger_post(post: schemas.BloggerPostBase, db: Session = Depends(get_db)):
    """Create Blogger post."""
    return crud.create_blogger_post(db=db, post=post)


@app.get("/blogger_posts/", response_model=List[schemas.BloggerPost], summary='Get list of Blogger posts')
def read_blogger_post(db: Session = Depends(get_db)):
    """Read Blogger posts."""
    return crud.get_blogger_posts(db=db)


@app.post("/blogger_items/", response_model=schemas.BloggerItem, summary='Create Blogger Item')
def create_blogger_item(item: schemas.BloggerItemBase, db: Session = Depends(get_db)):
    """Create Blogger Item."""
    return crud.create_blogger_item(db=db, blogit=item)


@app.get("/blogger_items/", response_model=List[schemas.BloggerItem], summary='Get list of Blogger Items')
def read_blogger_items(db: Session = Depends(get_db), tmdb_id: Optional[str] = None):
    """Read Blogger posts."""
    return crud.get_blogger_items(db=db, tmdb_id=tmdb_id)


@app.patch("/blogger_items/{item_id}", response_model=schemas.BloggerItem)
def update_blogger_item(updated_item: schemas.BloggerItemUpdate, item_id: str, db: Session = Depends(get_db)):
    """Update Item."""
    db_item = crud.get_blogger_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return crud.update_blogger_item(db=db, item=updated_item, stored_item=db_item)


@app.get("/blogger_items/{item_id}", response_model=schemas.BloggerItem)
def read_blogger_item(item_id: str, db: Session = Depends(get_db)):
    """Read single blogger item."""
    db_item = crud.get_blogger_item(db=db, item_id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item