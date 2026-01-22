# Gift Discovery + Recommendation Service Backend
This project implements a simple backend for gift discovery using a recommendation system. No external AI APIs are used, however are easy to implement. Logic is deterministic, and the design prioritizes readability and extensibility. The system allows:
- Ingesting a product catalog
- Searching and filtering products
- Generating personalized gift recommendations
- Logging user interaction events
- Improving recommendations over time using behavioral signals

## Running the Program
To run the program, write
```
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
In your terminal, then visit
```
http://127.0.0.1:8000/docs
```
for interactive API documentation via Swagger.

## Tech Stack
- Python + FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Uvicorn

## Project Structure:
```
app/
├─ crud.py
├─ database.py
├─ main.py
├─ models.py
├─ recommender.py
├─ schemas.py
data/
├─ products.json
app.db
requirements.txt
```

## API Endpoints

### POST /ingest

Ingests products from a local JSON file (products.json) into the database. Duplicate products are skipped based on URL.

**Input:** No request body, reads from data/products.json

**Output:**
```
 {
    "inserted": 2,
    "skipped": 0
 }
```

### GET /search
Searches and filters products in the catalog.

**Input:** Query Parameters (all optional):
- q: keyword search
- category: filter by category
- retailer: filter by retailer
- minPrice: minimum price
- maxPrice: maximum price
- sort: price_asc or price_desc

**Output:** Returns a list of matching products.

### POST /recommendations
Generates ranked gift recommendations based on recipient context, interests, and learned behavior.

**Input Example (JSON body):**
```
{
  "recipientAge": 25,
  "occasion": "Birthday",
  "relationship": "friend",
  "budget": 150,
  "interests": ["tech", "coffee"]
}
```

Optional Query Parameter:
userId – enables personalized learning boosts

**Output:** A ranked list of recommended products, including a score and human-readable explanation.

### POST /events
Logs user interactions with products; events are used to improve future recommendations.

**Input Example:**
```
{
  "userId": "user-123",
  "productId": 1,
  "eventType": "save_product"
}
```

**Output:**
```
{"status": logged}
```

### GET /recommendations/diagnostics
Provides insight into how the recommendation system is learning from user and global behavior.

**Input:**
userId (query parameter)

**Output:** Top inferred categories, boosted products, and an explanation of the learning logic.

## Recommendation Logic
Recommendations are generated using a weighted scoring system that considers budget alignment, interest overlap via tags, and light occasion/relationship heuristics. This approach is deterministic, explainable, and easy to extend with ML or LLM-based explanation generation in the future.

## Design Rationale
- The system prioritizes clarity and intuitivity.
- Recipient attributes (age, occasion, relationship) are accepted as structured inputs and treated as future features.
- The architecture cleanly separates concerns, making it easy to extend or replace components

## Future Improvements
- Implement ML model to learn from user inputs and events
- Create an intuitive user interface


