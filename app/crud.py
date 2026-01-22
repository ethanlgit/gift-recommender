from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate
from sqlalchemy import or_

from app.models import Event
from app.schemas import EventCreate
from sqlalchemy.orm import Session

# Create, Read, Update, Delete

def create_product(db: Session, product: ProductCreate):

    existing = db.query(Product).filter(Product.url == product.url).first()
    if existing:
        return None
    
    db_product = Product(
        title=product.title,
        description=product.description,
        price=product.price,
        brand=product.brand,
        category=product.category,
        retailer=product.retailer,
        url=product.url,
        tags=",".join(product.tags)
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product



def search_products(
        db: Session,
        q: str | None,
        category: str | None,
        retailer: str | None,
        min_price: float | None,
        max_price: float | None,
        sort: str | None
):
    query = db.query(Product)

    if q:
        query = query.filter(
            or_(
                Product.title.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%"),
                Product.tags.ilike(f"%{q}%")
            )
        )
    
    if category:
        query = query.filter(Product.category == category)
    
    if retailer:
        query = query.filter(Product.retailer == retailer)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())



    return query.all()



def create_event(db: Session, event: EventCreate):
    db_event = Event(
        user_id=event.userId,
        product_id=event.productId,
        event_type=event.eventType,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

