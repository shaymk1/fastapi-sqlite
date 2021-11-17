

from fastapi import FastAPI, APIRouter, Response, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, database
from fastapi.params import Depends
from sqlalchemy.orm import Session
from product.database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from ..schemas import TokenData


def get_db():
    # session gives us a connection to a database and we make an instance of it
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()

# hashing password
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRETE KEY FROM THE OPENSSL

SECRET_KEY = '32abc35c7e37273d678cebdc0497810d3daeef0743a1482c37446360cc0480d8'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


# utility function:
def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login')
#change schemas.Login into Oath2passwordrequestform
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(
        models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Username not found, or invalid user')
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    # generate jwt token for the user
    access_token = generate_token(
        data={"sub": seller.username}
    )

    return {'access_token': access_token, 'token_type': "bearer"}


# function to make sure that the current user has the token
def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid auth credentials', headers={'www-authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')  # extracting username from token
        if username is None:
            raise credentials_exception
        # if username exists,pass it into token_data
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
