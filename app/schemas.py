from pydantic import BaseModel
from typing import List

# Define what data the API accepts, what data it returns

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    brand: str
    category: str
    retailer: str
    url: str
    tags: List[str]



class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: float
    brand: str
    category: str
    retailer: str
    url: str
    tags: str

    class Config:
        from_attributes = True



class RecommendationRequest(BaseModel):
    recipientAge: int
    occasion: str
    relationship: str
    budget: float
    interests: List[str]



class RecommendationOut(BaseModel):
    product: ProductOut
    score: float
    reason: str



class EventCreate(BaseModel):
    userId: str
    productId: int
    eventType: str
