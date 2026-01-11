import csv
import random
import os

NUM_PRODUCTS = 100_000
NUM_SELLERS = 100_000  # match Seller table
MAX_SELLERS_PER_PRODUCT = 3
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/product_seller"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load product prices
product_price = {}
with open('data/product/product.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, start=1):
        product_price[idx] = float(row['price'])

file_index = 1
row_count = 0

outfile = open(f'{OUTPUT_DIR}/product_seller_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerow(['product_id', 'seller_id', 'supply_price'])

for product_id in range(1, NUM_PRODUCTS + 1):
    seller_count = random.randint(1, MAX_SELLERS_PER_PRODUCT)
    sellers = random.sample(range(1, NUM_SELLERS + 1), seller_count)
    
    for seller_id in sellers:
        if row_count >= BATCH_SIZE:
            outfile.close()
            file_index += 1
            row_count = 0
            outfile = open(f'{OUTPUT_DIR}/product_seller_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(outfile)
            writer.writerow(['product_id', 'seller_id', 'supply_price'])
        
        # realistic supply price with slight randomization
        margin_factor = random.uniform(0.5, 0.95)
        supply_price = round(product_price[product_id] * margin_factor, 2)
        writer.writerow([product_id, seller_id, supply_price])
        row_count += 1

outfile.close()
print(f"Product_Seller CSVs generated successfully in {OUTPUT_DIR}")
