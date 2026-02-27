import pandas as pd

def get_financial_advice(product_name, local_price, online_price):
    """
    "Online delivery takes 2 days. You have it on the shelf NOW. Suggest a 
    'Convenience Bundle' (e.g., Coffee + Local Milk) for 5% off."
    """
    price_gap = local_price - online_price
    
    if price_gap > 0:
        return f"Warning! {product_name} is ${price_gap:.2f} cheaper online. Suggestion: Bundle it with a local item or offer a 'Fresh Today' discount."
    else:
        return f"Great job! You are competitive on {product_name}. Highlight this in your next social media post!"

# Test logic (We will connect this to the UI later)
if __name__ == "__main__":
    print(get_financial_advice("Coffee", 15.00, 12.50))