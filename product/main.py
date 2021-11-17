
from fastapi import FastAPI, Response, status, HTTPException
from . import models
from .database import engine, SessionLocal
from .routers import product_api, seller_api, login_api

# from . import schemas
# from fastapi.params import Depends
# from sqlalchemy.orm import Session
# from typing import List
# from passlib.context import CryptContext


# we can also add metadata here
app = FastAPI(
    title="products API",
    description="Get details for all our products on a website",
    terms_of_service="http://www.myapi.com",
    contact={
        "developer name": "Shay",
        "website": "http://www.myapi.com",
        "email": "blah@gmail.com",
    },
    license_info={
        "name": "MIT",
        " url": "http://www.myapi.com"
    }
    # if i wana change the url for the docs
    # docs_url = "/mydocs" , redoc_url = None
)

app.include_router(product_api.router)
app.include_router(seller_api.router)
app.include_router(login_api.router)

models.Base.metadata.create_all(engine)



