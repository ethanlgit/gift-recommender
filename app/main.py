from fastapi import FastAPI
# get_db
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import ProductCreate
from app.crud import create_product

from app.database import engine
from app import models
from app.database import SessionLocal
from app.models import Product

from typing import Optional
from app.schemas import ProductOut
from app.crud import search_products

from app.schemas import RecommendationRequest, RecommendationOut
from app.recommender import score_product
from app.models import Product

from app.recommender import (
    score_product,
    get_user_category_boosts,
    get_global_product_boosts,
)

from app.schemas import EventCreate
from app.crud import create_event

# receive requests, validate inputs, call helper functions, return responses

app = FastAPI(title="Gift Discovery API")
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}


# ---------- Temporary (Testing Only) ---------------
# @app.post("/debug/add-product")
# def add_product():
#     db = SessionLocal()
#     product = Product(
#         title="Wireless Headphones",
#         description="Noise cancelling",
#         price=99.99,
#         brand="SoundCo",
#         category="Tech",
#         retailer="Amazon",
#         url="https://example.com/headphones",
#         tags="audio,tech"
#     )
#     db.add(product)
#     db.commit()
#     return {"ok": True}
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@app.post("/ingest")
def ingest_products(db: Session = Depends(get_db)):
    with open("data/products.json") as f:
        products = json.load(f)

    inserted = 0
    skipped = 0

    for p in products:
        product = ProductCreate(**p)
        result = create_product(db, product)

        if result:
            inserted += 1
        else:
            skipped += 1

    return {
        "inserted": inserted,
        "skipped": skipped
    }



@app.get("/search", response_model=list[ProductOut])
def search(
    q: Optional[str] = None,
    category: Optional[str] = None,
    retailer: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return search_products(
        db=db,
        q=q,
        category=category,
        retailer=retailer,
        min_price=minPrice,
        max_price=maxPrice,
        sort=sort,
    )



@app.post("/recommendations", response_model=list[RecommendationOut])
def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    userId: str | None = None,
):
    products = db.query(Product).all()
    
    category_boosts = get_user_category_boosts(db, userId) if userId else {}
    global_boosts = get_global_product_boosts(db)

    scored = []

    for product in products:
        score, reason = score_product(product, request)

        # User preference boost
        if userId and product.category in category_boosts:
            boost = category_boosts[product.category]
            score += boost
            reason += f"; boosted by past interest in {product.category}"

        # Global popularity boost
        if product.id in global_boosts:
            score += min(global_boosts[product.id], 3)
            reason += "; popular with other users"

        if score > 0:
            scored.append({
                "product": product,
                "score": score,
                "reason": reason
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:10]



@app.post("/events")
def log_event(
    event: EventCreate,
    db: Session = Depends(get_db),
):
    create_event(db, event)
    return {"status": "logged"}



@app.get("/recommendations/diagnostics")
def recommendation_diagnostics(
    userId: str,
    db: Session = Depends(get_db),
):
    category_boosts = get_user_category_boosts(db, userId)
    global_boosts = get_global_product_boosts(db)

    return {
        "top_categories": category_boosts.most_common(3),
        "top_boosted_products": global_boosts.most_common(3),
        "explanation": (
            "Recommendations are boosted based on user interaction history "
            "and globally popular products."
        )
    }
