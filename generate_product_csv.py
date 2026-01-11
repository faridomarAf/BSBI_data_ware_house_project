import csv
import random
import os

# ---------------- CONFIG ----------------
NUM_PRODUCTS = 100_000
OUTPUT_DIR = "data/product"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read categories
categories = []
with open('data/category/category.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        categories.append(row[0])

# Product templates per category
product_templates = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "4K TV", "Bluetooth Speaker"],
    "Books": ["Handbook", "Novel", "Cookbook", "Biography", "Guide"],
    "Clothing": ["T-Shirt", "Jacket", "Jeans", "Hoodie", "Dress"],
    "Home & Kitchen": ["Frying Pan", "Coffee Maker", "Bed Sheets", "Vacuum Cleaner", "Blender"],
    "Sports": ["Football", "Tennis Racket", "Yoga Mat", "Dumbbell Set", "Basketball"],
    "Health": ["Vitamin C", "Protein Powder", "Fitness Tracker", "Supplement Pack", "Thermometer"],
    "Beauty": ["Lipstick", "Cream", "Perfume", "Nail Polish", "Shampoo"],
    "Toys": ["Lego Set", "Puzzle", "Action Figure", "Board Game", "RC Car"],
    "Automotive": ["Car Charger", "LED Headlights", "Tire Pump", "Car Mat", "Air Freshener"],
    "Grocery": ["Organic Pasta", "Olive Oil", "Coffee Beans", "Cereal", "Honey"]
}

filename = f"{OUTPUT_DIR}/product.csv"
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['product_name', 'price', 'category_id'])

    for i in range(1, NUM_PRODUCTS + 1):
        # Randomly select category
        category_id = random.randint(1, len(categories))
        category_name = categories[category_id-1]

        # Pick a realistic product name for that category
        template = random.choice(product_templates[category_name])
        product_name = f"{template} {random.randint(100, 999)}"

        # Category-based price
        if category_name == "Electronics":
            price = round(random.uniform(50, 1000), 2)
        elif category_name == "Books":
            price = round(random.uniform(5, 50), 2)
        elif category_name == "Grocery":
            price = round(random.uniform(1, 50), 2)
        else:
            price = round(random.uniform(10, 500), 2)

        writer.writerow([product_name, price, category_id])

print(f"Generated {filename}")
