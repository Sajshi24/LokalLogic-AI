from fastapi import FastAPI
from .ai_engine import get_financial_advice

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "LokalLogic AI is online"}

@app.get("/analyze/{product_id}")
def analyze_product(product_id: int):
    # For the hackathon, we are mocking the online price check
    # In Step 4, we will add the real scraper!
    return {
        "product_id": product_id,
        "advice": "Checking market trends... All looks good!"
    }
