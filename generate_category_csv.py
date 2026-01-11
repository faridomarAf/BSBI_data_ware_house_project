import csv
import os

categories = [
    'Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports',
    'Health', 'Beauty', 'Toys', 'Automotive', 'Grocery'
]

OUTPUT_DIR = "data/category"
os.makedirs(OUTPUT_DIR, exist_ok=True)

filename = f"{OUTPUT_DIR}/category.csv"

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['category_name'])
    for cat in categories:
        writer.writerow([cat])

print(f"Generated {filename}")
