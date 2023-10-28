from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload, subqueryload
from . import models, schema
from decimal import Decimal

# Order
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_order(db: Session, order: schema.OrderCreate, buyer_id: int):
    total_price = 0
    for item in order.order_items:
        product = get_product(db=db, product_id=item.product_id)
        unit_price = product.price
        quantity = item.quantity
        total_price += unit_price * quantity

    db_order = models.Order(
        seller_id=order.seller_id,
        status='Pending',
        total_price=total_price,
        buyer_id=buyer_id
    )

    db.add(db_order)
    db.commit()

    for item in order.order_items:
        db_item = models.OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            order_id=db_order.id,
            price_per_item=unit_price
        )
        db.add(db_item)

    db_order.delivery_charge = 10
    db_order.tax = db_order.total_price * Decimal(0.18)  # 18% tax
    db_order.gross_total = db_order.total_price + db_order.tax + db_order.delivery_charge

    db.commit()
    db.refresh(db_order)
    
    return db_order

# Product
def get_products_for_seller(db: Session, seller_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Product).join(models.product_seller).filter(models.product_seller.c.seller_id == seller_id).offset(skip).limit(limit).all()

def create_seller_product(db: Session, product: schema.ProductCreate, seller_id: int):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Add the product to the seller's products
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    db_seller.products.append(db_product)
    
    db.commit()
    
    return db_product

# Seller
def create_seller(db: Session, seller: schema.SellerCreate):
    db_seller = models.Seller(**seller.model_dump())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

def get_seller_by_phone(db: Session, phone_number: str):
    return db.query(models.Seller).filter(models.Seller.phone_number == phone_number).first()

def get_seller(db: Session, id: int):
    return db.query(models.Seller).filter(models.Seller.id == id).first()

def validate_category(category: str, allowed_categories: list = models.CATEGORY_CHOICES):
    return category in allowed_categories

def update_seller(db: Session, seller: schema.SellerUpdate, seller_id: int):
    if not validate_category(seller.model_dump()["category"]):
        raise HTTPException(status_code=400, detail="Invalid category")    
    
    db.query(models.Seller).filter(models.Seller.id == seller_id).update(seller.model_dump())
    db.commit()
    return get_seller(db, seller_id)

def get_all_sellers(db: Session):
    return db.query(models.Seller).all()

def get_sellers_by_category(db: Session, category: str):
    return db.query(models.Seller).filter(models.Seller.category == category).options(joinedload(models.Seller.products)).all()

# Address
def get_address(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id == id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()

def validate_address(address: dict, allowed_areas: list = models.AREA_CHOICES):
    return address["area"] in allowed_areas

def create_buyer_address(db: Session, address: schema.AddressCreate, buyer_id: int):
    if not validate_address(address.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid area")
    
    db_address = models.Address(**address.model_dump(), owner_id=buyer_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_buyer_address(db: Session, address: schema.AddressUpdate):
    if not validate_address(address.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid area")
    
    db.query(models.Address).filter(models.Address.id == address.id).update(address.model_dump())
    db.commit()
    return get_address(db, id=address.id)

def delete_buyer_address(db: Session, id: int):
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

# Buyer
def get_buyer_by_phone(db: Session, phone_number: str):
    return db.query(models.Buyer).filter(models.Buyer.phone_number == phone_number).first()

def create_buyer(db: Session, buyer: schema.BuyerCreate):
    db_buyer = models.Buyer(phone_number=buyer.phone_number)
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer

def get_buyer(db: Session, buyer_id: int):
    buyer = db.query(
        models.Buyer
    ).filter(
        models.Buyer.id == buyer_id
    ).options(
        joinedload(models.Buyer.addresses)
    ).first()
    
    if buyer is not None:
        buyer.addresses.sort(key=lambda address: address.id, reverse=True)
    
    return buyer
