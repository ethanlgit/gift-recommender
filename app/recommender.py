from app.models import Product
from collections import Counter
from sqlalchemy.orm import Session
from app.models import Event, Product

# scoring rules, learning layer logic, signal aggregation

def score_product(product, request):
    """
    STRONG opportunity to implement machine learning techniques!
    """

    score = 0
    reasons = []

    # Budget filter
    if product.price and product.price > request.budget:
        return 0, "Over budget"

    score += 2
    reasons.append("Within budget")

    # Interest match
    if product.tags:
        tags = product.tags.lower().split(",")
        matches = set(tags) & set(i.lower() for i in request.interests)
        if matches:
            score += len(matches) * 2
            reasons.append(f"Matches interests: {', '.join(matches)}")

    # Occasion rules
    if request.occasion.lower() == "birthday":
        score += 1
        reasons.append("Good for birthdays")

    if request.occasion.lower() == "anniversary" and product.category in ["Jewelry", "Fashion"]:
        score += 2
        reasons.append("Good for anniverseries")

    # relationship rules
    if request.relationship.lower() in ["partner", "spouse"] and product.price > 50:
        score += 1
        reasons.append("Good for close relationships")

    if request.relationship.lower() == "coworker" and product.price < 40:
        score += 1
        reasons.append("Good for coworker")

    # age rules
    if request.recipientAge < 18 and product.category == "Toys":
        score += 2
        reasons.append("Age-appropriate")

    if request.recipientAge > 50 and product.category in ["Home", "Wellness"]:
        score += 1
        reasons.append("Popular for this age group")

    return score, "; ".join(reasons)



def get_user_category_boosts(db: Session, user_id: str) -> dict:
    events = (
        db.query(Event)
        .join(Product)
        .filter(Event.user_id == user_id)
        .filter(Event.event_type.in_(["save_product", "click_out"]))
        .all()
    )

    categories = [e.product.category for e in events]
    return Counter(categories)



def get_global_product_boosts(db: Session) -> dict:
    events = (
        db.query(Event)
        .filter(Event.event_type.in_(["save_product", "click_out"]))
        .all()
    )

    product_counts = Counter(e.product_id for e in events)
    return product_counts
