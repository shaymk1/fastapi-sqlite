
from pydantic import BaseModel


class Product(BaseModel):
    title:str
    description : str
    price: int


#if you want some fields not to display
class DisplayProduct(BaseModel):
    title: str
    description: str
    class Config:
        orm_mode = True

class Seller(BaseModel):
    username: str
    email:str
    password:str

    
    
        