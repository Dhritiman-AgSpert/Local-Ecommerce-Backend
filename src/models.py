from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String, index=True)
    phone_number = Column(String, index=True)
    count = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
