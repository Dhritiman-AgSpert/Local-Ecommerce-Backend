from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from .. import crud, models, schema
from ..database import get_db
from .auth import get_current_seller

router = APIRouter()

@router.post('', response_model=schema.Product)
def create_product_for_seller(
    product: schema.ProductCreate, 
    current_seller: models.Seller = Depends(get_current_seller),
    db: Session = Depends(get_db),
):
    return crud.create_seller_product(db=db, product=product, seller_id=current_seller.id)

@router.get('', response_model=List[schema.Product])
def read_products_for_seller(
    skip: int = 0, 
    limit: int = 100, 
    current_seller: models.Seller = Depends(get_current_seller),
    db: Session = Depends(get_db),
):
    products = crud.get_products_for_seller(db=db, seller_id=current_seller.id, skip=skip, limit=limit)
    return products