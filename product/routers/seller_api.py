
from fastapi import FastAPI, APIRouter, Response, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from product.database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext


router = APIRouter(
    tags=['sellers']
)

#hashing password
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_db():
    # session gives us a connection to a database and we make an instance of it
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/sellers', response_model=schemas.DisplaySeller)
def create_sellers(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(
        username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
