
from fastapi import FastAPI, Response, status, HTTPException
from . import schemas
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    #session gives us a connection to a database and we make an instance of it
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#getting data from the database
@app.get('/products')
def get_products(db: Session = Depends(get_db)): #because we want to have access to all our data on db
    products = db.query(models.Product).all()
    return products

#getting a single product by its id
@app.get('/product/{id}', response_model = schemas.DisplayProduct)
def get_product(id, response: Response, db: Session = Depends(get_db)):
    single_product = db.query(models.Product).filter(models.Product.id==id).first() 
    if not single_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='product not found!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'product not found!'}
    return single_product

#deleting a product
@app.delete('/delete/{id}')
def delete_product(id, db: Session = Depends(get_db)):
    single_product = db.query(models.Product).filter(
        models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted!'}

#update a product
@app.put('/products/{id}')
def update(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id==id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return{'product successfully updated'}
    
    

#inserting/adding data into the database
@app.post('/product')
def add(request: schemas.Product, db: Session = Depends(get_db)):
    #creating a product object by making use of the product model
    new_product = models.Product(title=request.title, description=request.description, price=request.price)
    db.add(new_product)#insert the product in the db
    db.commit()#commit the changes
    db.refresh(new_product)#let it refresh
    return request



#for the sellers now

@app.post('/sellers')
def create_sellers(request:schemas.Seller):
    return request
