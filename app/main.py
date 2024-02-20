from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, database

# Create an instance of FastAPI
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create an item
@app.post("/items/")
async def create_item(name: str, description: str, db: Session = Depends(get_db)):
    return crud.create_item(db=db, name=name, description=description)

# Get an item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

