import csv
import glob
import random
import os
from datetime import datetime, timedelta

# -----------------------------------
# CONFIG
# -----------------------------------
PAYMENT_BATCH_SIZE = 100_000
PAYMENT_METHODS = ['Credit Card', 'PayPal', 'SEPA Transfer', 'Invoice']

# Folder structure
PRODUCT_FILE = 'data/product/product.csv'
ORDER_ITEMS_DIR = 'data/order_items'
ORDERS_DIR = 'data/orders'
OUTPUT_DIR = 'data/payments'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------
# STEP 1: Load product prices
# -----------------------------------
product_price = {}
with open(PRODUCT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    product_id = 1
    for row in reader:
        product_price[product_id] = float(row['price'])
        product_id += 1
print(f"Loaded prices for {len(product_price)} products")

# -----------------------------------
# STEP 2: Aggregate order totals from order_items
# -----------------------------------
order_totals = {}

for file in glob.glob(f'{ORDER_ITEMS_DIR}/order_item_part_*.csv'):
    print(f"Processing {file} ...")
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_id = int(row['order_id'])
            product_id = int(row['product_id'])
            quantity = int(row['quantity'])
            amount = product_price[product_id] * quantity
            order_totals[order_id] = order_totals.get(order_id, 0) + amount

print(f"Aggregated totals for {len(order_totals)} orders")

# -----------------------------------
# STEP 3: Generate payments CSVs
# -----------------------------------
file_index = 1
row_count = 0

outfile = open(f'{OUTPUT_DIR}/payment_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerow(['order_id', 'amount', 'payment_method', 'payment_status', 'payment_date'])

for file in glob.glob(f'{ORDERS_DIR}/orders_part_*.csv'):
    print(f"Reading {file} ...")
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_id = int(row['order_id'])
            status = row['order_status']

            # Skip cancelled orders
            if status == 'Cancelled':
                continue

            # Rotate file for batching
            if row_count >= PAYMENT_BATCH_SIZE:
                outfile.close()
                file_index += 1
                row_count = 0
                outfile = open(f'{OUTPUT_DIR}/payment_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
                writer = csv.writer(outfile)
                writer.writerow(['order_id', 'amount', 'payment_method', 'payment_status', 'payment_date'])

            # Payment status logic
            payment_status = 'Completed' if status in ['Delivered', 'Shipped'] else 'Pending'

            # Payment date in MySQL DATETIME format (random past 2 years)
            payment_date = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d %H:%M:%S")

            # Write row
            writer.writerow([
                order_id,
                round(order_totals.get(order_id, 0), 2),
                random.choice(PAYMENT_METHODS),
                payment_status,
                payment_date
            ])

            row_count += 1

outfile.close()
print(f"Payments generated in {file_index} files at {OUTPUT_DIR}")
