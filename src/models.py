from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Enum, Numeric, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from .database import Base

import datetime
import pytz

ORDER_STATUSES = [
    'Creating',
    'Pending',
    'Placed',
    'Shipped', 
    'Delivered', 
    'Cancelled'
]
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Numeric(precision=10, scale=2), nullable=False)
    tax = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    delivery_charge = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    status = Column(Enum(*ORDER_STATUSES, name='order_statuses'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')))

    # Relationships
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    buyer = relationship("Buyer", back_populates="orders")
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Numeric(precision=10, scale=2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    order_id = Column(Integer, ForeignKey('orders.id'))
    product = relationship("Product")
    product_id = Column(Integer, ForeignKey('products.id'))

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Numeric(precision=10, scale=2), default=0.00)

    # Relationships
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="wallet")

PAYMENT_METHODS = ['UPI', 'Net-banking']
class PaymentInfo(Base):
    __tablename__ = "payment_info"

    id = Column(Integer, primary_key=True, index=True)
    
    # Fields for Net-banking
    bank_name = Column(String(64), nullable=True)
    account_holder_name = Column(String(256), nullable=True)
    account_number = Column(String(20), nullable=True)
    ifsc_code = Column(String(11), nullable=True)

    # Field for UPI
    upi_id = Column(String(256), nullable=True)

    # Field to indicate the payment method chosen by the seller
    payment_method = Column(Enum(*PAYMENT_METHODS, name='payment_method'), nullable=False)

    # Relationships
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="payment_info")

# Association table
product_seller = Table(
    'product_seller',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('seller_id', Integer, ForeignKey('sellers.id'))
)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(256), nullable=True)
    sub_category = Column(String(256), nullable=True)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(1024))
    unit = Column(String(32), nullable=False)
    moq = Column(Numeric(precision=6, scale=2), nullable=False)
    factor = Column(Numeric(precision=6, scale=2), nullable=False)
    weight = Column(Numeric(precision=8, scale=2), nullable=False)
    image_url = Column(String(256), nullable=False)
    price = Column(Numeric(precision=6, scale=2), CheckConstraint('price >= 0'), nullable=False)

    # Relationships
    sellers = relationship("Seller", secondary=product_seller, back_populates="products")

CATEGORY_CHOICES = [
    "Grocery",
    "Meat"
]
class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(*CATEGORY_CHOICES, name='category'), nullable=True)
    name = Column(String(256), nullable=True)
    phone_number = Column(String(10), nullable=False, unique=True)
    image_url = Column(String, nullable=True)
    trade_license = Column(String(64), nullable=True)
    address = Column(String(512), nullable=True)
    lat = Column(Numeric(precision=9, scale=6), nullable=True)
    lng = Column(Numeric(precision=9, scale=6), nullable=True)
    
    # Relationships
    products = relationship("Product", secondary=product_seller, back_populates="sellers")
    payment_info = relationship("PaymentInfo", uselist=False, back_populates="seller")
    wallet = relationship("Wallet", uselist=False, back_populates="seller")
    orders = relationship("Order", back_populates="seller")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)

AREA_CHOICES = [
    "Lachit Nagar"
]
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    phone_number = Column(String(10), nullable=False)
    house = Column(String(256), nullable=False)
    street = Column(String(256), nullable=False)
    area = Column(Enum(*AREA_CHOICES, name='area'), nullable=False)
    city = Column(String(256), nullable=False)
    pincode = Column(String(6), nullable=False)
    lat = Column(Numeric(precision=9, scale=6), nullable=False)
    lng = Column(Numeric(precision=9, scale=6), nullable=False)

    # Relationships
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

    # Relationships
    addresses = relationship(
        "Address",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True,
    )
    orders = relationship("Order", back_populates="buyer")
