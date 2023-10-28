from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schema, database
from .auth import get_current_buyer

router = APIRouter()

@router.post("", response_model=schema.Order)
def create_order(order: schema.OrderCreate, buyer: schema.Buyer = Depends(get_current_buyer), db: Session = Depends(database.get_db)):
    return crud.create_order(db=db, order=order, buyer_id=buyer.id)