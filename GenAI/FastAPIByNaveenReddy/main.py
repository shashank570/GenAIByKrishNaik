from fastapi import FastAPI, Depends
from models import Product
import database_model
from database import engine, session
from sqlalchemy.orm import Session

app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello bhai sahab kaise hai aap"


products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price= 999.99, quantity=30),
    Product(id=3, name="Pen", description="A Blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_model.Product).count()
    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
        db.commit() 

init_db()

@app.get("/products")
def get_all_products(db : Session = Depends(get_db)): # dependency ingection
    # db = session()
    # db.query()
    db_products = db.query(database_model.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id : int, db : Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product
    return "No Product Found"

@app.post("/product")
def add_product(product : Product, db : Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/product/{id}")
def update_product(id : int, product : Product, db : Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated Successfully"
    return "No Product Found"


@app.delete("/product/{id}")
def delete_product(id : int, db : Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"
    return "No Product Found"


