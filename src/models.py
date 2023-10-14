from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    addresses = relationship(
        "Address",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True,
    )
    
class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String, index=True)
    phone_number = Column(String, index=True)
    count = Column(Integer, default=0)
    verified = Column(Boolean, default=False)


PINCODE_CHOICES = [
    "781007"
]

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    phone = Column(String(10), nullable=False)
    house = Column(String(256), nullable=False)
    street = Column(String(256), nullable=False)
    area = Column(String(256), nullable=False)
    city = Column(String(256), nullable=False)
    pincode = Column(Enum(*PINCODE_CHOICES, name='pincode'), nullable=False)
    lat = Column(Numeric(precision=9, scale=6), nullable=False)
    lng = Column(Numeric(precision=9, scale=6), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="addresses")