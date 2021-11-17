

from fastapi import FastAPI, APIRouter, Response, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from product.routers.login_api import get_current_user
from .. import models, schemas
from product.database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext


router = APIRouter(
    tags=['products'],
    prefix="/product"  # to help you with the route
)


def get_db():
    # session gives us a connection to a database and we make an instance of it
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
# because we want to have access to all our data on db
def get_products(db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

# getting a single product by its id


@router.get('/{id}', response_model=schemas.DisplayProduct)
def get_product(id, response: Response, db: Session = Depends(get_db)):
    single_product = db.query(models.Product).filter(
        models.Product.id == id).first()
    if not single_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='product not found!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'product not found!'}
    return single_product

# deleting a product


@router.delete('/{id}')
def delete_product(id, db: Session = Depends(get_db)):
    single_product = db.query(models.Product).filter(
        models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted!'}

# update a product


@router.put('/{id}')
def update(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return{'product successfully updated'}


# inserting/adding data into the database
@router.post('/')
def add(request: schemas.Product, db: Session = Depends(get_db)):
    # creating a product object by making use of the product model
    new_product = models.Product(
        title=request.title, description=request.description, price=request.price, seller_id=1)
    db.add(new_product)  # insert the product in the db
    db.commit()  # commit the changes
    db.refresh(new_product)  # let it refresh
    return request
