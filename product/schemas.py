
from pydantic import BaseModel


class Product(BaseModel):
    title: str
    description: str
    price: int


# if you want some fields not to display,  you create response model

class DisplaySeller(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
class DisplayProduct(BaseModel):
    title: str
    description: str
    seller: DisplaySeller

    class Config:
        orm_mode = True


class Seller(BaseModel):
    username: str
    email: str
    password: str

# response model



