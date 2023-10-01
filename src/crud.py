from sqlalchemy.orm import Session
from . import models, schema

def get_user_by_phone(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_otp_by_phone(db: Session, phone_number: str):
    return db.query(models.OTP).filter(models.OTP.phone_number == phone_number).first()

def create_otp(db: Session, otp: schema.OTPCreate):
    db_otp = models.OTP(otp=otp.otp, phone_number=otp.phone_number, count=otp.count)
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp
