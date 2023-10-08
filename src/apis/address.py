from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schema, crud, database, models

from .auth import get_current_user

router = APIRouter()


@router.get('/allowed_pincodes')
def allowed_pincodes(
    _: schema.User = Depends(get_current_user)
):
    return models.PINCODE_CHOICES

@router.post('', response_model=schema.Address)
def create_address_for_user(
    address: schema.AddressCreate, db: Session = Depends(database.get_db), current_user: schema.User = Depends(get_current_user)
):
    return crud.create_user_address(db=db, address=address, user_id=current_user.id)

@router.put('{id}', response_model=schema.Address)
def update_address(id: int, address: schema.AddressUpdate, db: Session = Depends(database.get_db)):
    db_address = crud.get_address(db=db, id=id)
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return crud.update_user_address(db=db, address=address)

@router.delete('{id}')
def delete_address(id: int, db: Session = Depends(database.get_db)):
    db_address = crud.get_address(db=db, id=id)
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    crud.delete_user_address(db=db, id=id)
    
    return {"detail": "Address deleted"}