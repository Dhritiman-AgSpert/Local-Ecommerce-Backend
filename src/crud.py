from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from . import models, schema

# Address
def get_address(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id == id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()

def validate_address(address: dict, allowed_pincodes: list = models.PINCODE_CHOICES):
    return address["pincode"] in allowed_pincodes

def create_user_address(db: Session, address: schema.AddressCreate, user_id: int):
    if not validate_address(address.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid pincode")
    
    db_address = models.Address(**address.model_dump(), owner_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_user_address(db: Session, address: schema.AddressUpdate):
    if not validate_address(address.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid pincode")
    
    db.query(models.Address).filter(models.Address.id == address.id).update(address.model_dump())
    db.commit()
    return get_address(db, id=address.id)

def delete_user_address(db: Session, id: int):
    address = get_address(db, id=id)
    db.delete(address)
    db.commit()

# OTP
def get_otp_by_phone(db: Session, phone_number: str):
    return db.query(models.OTP).filter(models.OTP.phone_number == phone_number).first()

def create_otp(db: Session, otp: schema.OTPCreate):
    db_otp = models.OTP(otp=otp.otp, phone_number=otp.phone_number, count=otp.count)
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp

def update_otp(db: Session, otp: schema.OTPCreate):
    db_otp = db.query(models.OTP).filter(models.OTP.phone_number == otp.phone_number).first()
    if not db_otp:
        raise HTTPException(status_code=404, detail="OTP obj not found")
    for key, value in vars(otp).items():
        setattr(db_otp, key, value)
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp

# User
def get_user_by_phone(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).options(
        joinedload(models.User.addresses)
    ).first()
