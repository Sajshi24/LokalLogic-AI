from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import sys
import random

# --- PATH FIX START ---
# This tells Python to look inside the 'backend' folder for our scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_engine import get_financial_advice
from scraper import get_online_price
# --- PATH FIX END ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust path handling for Windows/OneDrive
current_dir = os.path.dirname(os.path.abspath(__file__))
# If main.py is in /backend, we go up one level to find /data
base_path = os.path.dirname(current_dir)
csv_path = os.path.join(base_path, "data", "inventory.csv")

inventory_df = pd.read_csv(csv_path)

@app.get("/")
def home():
    return {"message": "Backend is live"}

@app.get("/analyze/{product_id}")
def analyze_product(product_id: int):
    # Find product in CSV
    product_row = inventory_df[inventory_df['product_id'] == product_id]
    
    if product_row.empty:
        return {"error": "Product not found"}
    
    p_name = str(product_row.iloc[0]['product_name'])
    local_p = float(product_row.iloc[0]['local_price'])
    
    # Get Market Data
    online_p = get_online_price(p_name)
    advice = get_financial_advice(p_name, local_p, online_p)
    
    return {
        "product_name": p_name,
        "your_price": local_p,
        "online_price": online_p,
        "buddy_advice": advice
    }

@app.get("/weekly-summary")
def get_summary():
    return {
        "health_score": 85,
        "savings_detected": 120.50,
        "message": "Your shop is healthy! You saved $120 this week by matching online discounts."
    }

@app.get("/generate-marketing")
def generate_marketing(k1: str, k2: str, k3: str):
    # This logic forces the use of your k1 (Vibe), k2 (Product), and k3 (Benefit)
    # Using python f-strings to inject your exact inputs into the text
    
    caption = (
        f"✨ ATTENTION: EXPERIENCE THE {k1.upper()} VIBE! ✨\n\n"
        f"Looking for the best {k2} in town? Look no further! "
        f"We've combined our unique local touch with the {k3} quality "
        f"you've been waiting for.\n\n"
        f"Whether you're a long-time fan or a first-time visitor, "
        f"our new {k2} is designed specifically for you. "
        f"Stop by today and feel the {k1} difference! 🏠"
    )
    
    # Create hashtags by removing spaces from your keywords
    h1, h2, h3 = k1.replace(" ", ""), k2.replace(" ", ""), k3.replace(" ", "")
    hashtags = f"#{h1} #{h2} #{h3} #LocalLogic #BusinessGrowth"
    
    return {"caption": caption, "hashtags": hashtags}

@app.get("/ai-chat")
def ai_chat(query: str):
    # Pure reactive response logic
    query = query.lower()
    if "price" in query:
        return {"response": "Analysis shows your pricing is 8% above market. Reducing it by 3% could increase volume by 15%."}
    elif "sale" in query:
        return {"response": "Your weekend sales trend is up by 12%. I recommend restocking your top 3 items by Friday."}
    else:
        return {"response": f"I've processed your request regarding '{query}'. Based on your sales data, focus on high-margin items this month."}