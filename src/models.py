from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(String(1024))
    image_url = Column(String(256), nullable=False)
    price = Column(Numeric(precision=6, scale=2), CheckConstraint('price >= 0'), nullable=False)
    owner_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    owner = relationship("Seller", back_populates="products")

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(256), nullable=True)
    name = Column(String(256), nullable=True)
    phone = Column(String(10), nullable=False, unique=True)
    image_url = Column(String, nullable=True)
    trade_license = Column(String(64), nullable=True)
    address = Column(String(512), nullable=True)
    lat = Column(Numeric(precision=9, scale=6), nullable=True)
    lng = Column(Numeric(precision=9, scale=6), nullable=True)
    products = relationship(
        "Product",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True,
    )

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)

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
    owner_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    owner = relationship("Buyer", back_populates="addresses")

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String, index=True)
    phone_number = Column(String, index=True)
    count = Column(Integer, default=0)
    verified = Column(Boolean, default=False)

class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    addresses = relationship(
        "Address",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True,
    )
