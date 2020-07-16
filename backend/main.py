from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post('/users/', response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db, user=user)
