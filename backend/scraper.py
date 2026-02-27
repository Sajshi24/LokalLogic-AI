import requests
from bs4 import BeautifulSoup
import random

def get_online_price(product_name):
    """
    In a real-world app, this would search Google Shopping or Amazon.
    For the hackathon demo, we will simulate a 'Live Market' check.
    """
    # Mocking the volatility of e-commerce prices (2026 style)
    base_prices = {
        "Premium Coffee": 12.50,
        "Organic Milk": 3.80,
        "Local Honey": 14.00,
        "Whole Wheat Bread": 2.99
    }
    
    # Get the base price or a random value if product not found
    price = base_prices.get(product_name, random.uniform(5.0, 20.0))
    
    # Simulate a small random market fluctuation (-5% to +5%)
    fluctuation = random.uniform(0.95, 1.05)
    return round(price * fluctuation, 2)

# Test the scraper
if __name__ == "__main__":
    test_product = "Premium Coffee"
    print(f"Checking online price for {test_product}...")
    print(f"Online Price: ${get_online_price(test_product)}")