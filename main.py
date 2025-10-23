from sqlmodel import SQLModel, create_engine, Session, select, delete
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

@app.get("/product/{id}", response_model=ProductResponse,tags=["READ by ID"])
async def getProduct(id: int, db: Session= Depends(get_db)):
    stmt = select(Product).where(Product.id == id)
    result = db.exec(stmt).first()
    return ProductResponse.model_validate(result)


@app.get("/api/product", response_model=list[ProductResponse],tags=["READ all"])
async def getProducts(db: Session= Depends(get_db)):
    stmt = select(Product)
    result = db.exec(stmt).all()
    product_list = []
    for prod in result:
        if ProductResponse.model_validate(prod):
            product_list.append(prod)
    return product_list #El stock y el cost son datos sensibles


@app.get("/api/product/{filtro}", response_model=dict, tags=["READ by filter"])
async def getProduct(filtro: str, db: Session= Depends(get_db)):
    attr = getattr(Product, filtro)
    stmt = select(attr)
    result = db.exec(stmt).all()
    product_list = []
    for prod in result:
        product_list.append(prod)
    return {filtro: product_list}

@app.delete("/api/product/{id}", response_model=dict, tags=["DELETE by ID"])
async def deleteProduct(id: int, db:Session=Depends(get_db)):
    prod_delete = delete(Product).where(Product.id == id)
    db.exec(prod_delete)
    db.commit()
    return {"msg": "Producto eliminado"}

#    prod_delete = db.exec(select(Product).where(Product.id == id)).first()
#    if prod_delete:
#        db.delete(prod_delete)
#        db.commit()
#        return {"msg":"Usuario eliminado correctamente."}
#    else:
#        return {"msg":"Usuario no encontrado."}

@app.get("/api/productinfo/{id}", response_model=list[dict], tags=["partial READ"])
async def getPartialProducts(id:int,db: Session= Depends(get_db)):
    filtros = ["name", "cost", "stock"]
    attr = [getattr(Product, c) for c in filtros]
    stmt = select(*attr).where(Product.id == id)
    result = db.exec(stmt).all()
    res = [dict(zip(filtros, row)) for row in result]
    return res
