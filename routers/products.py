from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from pydantic import BaseModel
from sqlalchemy import func  # Importa func para agregaciones
from auth import get_current_user

router = APIRouter()

# Modelo Pydantic para productos
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    affiliate_link: str
    owner_id: int

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {"products": products}

@router.post("/")
def add_product(product: ProductCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        affiliate_link=product.affiliate_link,
        owner_id=product.owner_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added!", "product": new_product}

@router.post("/{product_id}/click")
def register_click(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.clicks += 1
    db.commit()
    return {"message": "Click registered", "product_id": product.id, "total_clicks": product.clicks}

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    total_clicks = db.query(func.sum(Product.clicks)).scalar()  # Cambiar a func.sum
    total_income = db.query(func.sum(Product.price)).scalar()  # Cambiar a func.sum

    return {
        "total_products": total_products,
        "total_clicks": total_clicks or 0,
        "total_income": total_income or 0.0,
    }