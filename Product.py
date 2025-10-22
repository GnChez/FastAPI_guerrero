from sqlmodel import SQLModel, Field

class Product(SQLModel, table= True):
    id: int | None =  Field(default=None, primary_key=True)
    name: str
    price: float
    description: str | None
    cost: float | None
    stock: int

class ProductRequest(SQLModel):
    name: str
    price: float
    description: str | None
    cost: float | None
    stock:int

class ProductResponse(SQLModel):
    id: int
    name: str
    price: float
    description: str | None