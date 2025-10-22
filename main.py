from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends
from Product import ProductRequest, Product, ProductResponse
app = FastAPI()

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.post("/product", response_model=dict, tags=["CREATE"])
async def addProduct(product: ProductRequest, db:Session = Depends(get_db)):
    insert_prod = Product.model_validate(product)
    db.add(insert_prod)
    db.commit()
    return {"msg":"Product added"}

@app.get("/user/{id}", response_model=ProductResponse,tags=["READ by ID"])
async def getProduct(id: int, db: Session= Depends(get_db)):
    stmt = select(Product).where(Product.id == id)
    result = db.exec(stmt).first()
    return ProductResponse.model_validate(result)