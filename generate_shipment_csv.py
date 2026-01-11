import csv
import glob
import random
import os
from datetime import timedelta
from dateutil import parser

# -----------------------------------
# CONFIG
# -----------------------------------
SHIPMENT_BATCH_SIZE = 100_000
COURIERS = ['DHL', 'Hermes', 'UPS', 'FedEx', 'GLS']

ORDERS_DIR = 'data/orders'
WAREHOUSE_FILE = 'data/warehouse/warehouse.csv'
OUTPUT_DIR = 'data/shipments'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------
# STEP 1: Load warehouse IDs
# -----------------------------------
warehouses = []
with open(WAREHOUSE_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, _ in enumerate(reader, start=1):
        warehouses.append(idx)

print(f"Loaded {len(warehouses)} warehouses")

# -----------------------------------
# STEP 2: Generate shipment CSVs
# -----------------------------------
file_index = 1
row_count = 0

outfile = open(f'{OUTPUT_DIR}/shipment_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerow(['order_id', 'warehouse_id', 'courier', 'shipped_date', 'delivery_status'])

for file in glob.glob(f'{ORDERS_DIR}/orders_part_*.csv'):
    print(f"Processing {file} ...")
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            order_id = int(row['order_id'])
            order_status = row['order_status']

            if order_status in ['Pending', 'Cancelled']:
                continue

            if row_count >= SHIPMENT_BATCH_SIZE:
                outfile.close()
                file_index += 1
                row_count = 0
                outfile = open(f'{OUTPUT_DIR}/shipment_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
                writer = csv.writer(outfile)
                writer.writerow(['order_id', 'warehouse_id', 'courier', 'shipped_date', 'delivery_status'])

            order_date = parser.parse(row['order_date'])
            shipped_date = order_date + timedelta(days=random.randint(0, 7))

            if order_status == 'Delivered':
                delivery_status = 'Delivered'
            elif order_status == 'Shipped':
                delivery_status = random.choice(['Shipped', 'Delivered'])
            else:
                delivery_status = 'Processing'

            writer.writerow([
                order_id,
                random.choice(warehouses),
                random.choice(COURIERS),
                shipped_date.strftime('%Y-%m-%d %H:%M:%S'),
                delivery_status
            ])

            row_count += 1

outfile.close()
print(f"Shipment CSVs generated in {file_index} files at {OUTPUT_DIR}")
