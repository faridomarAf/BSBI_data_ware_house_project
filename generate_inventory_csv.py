import csv
import random
import os

NUM_PRODUCTS = 100_000
WAREHOUSE_FILE = 'data/warehouse/warehouse.csv'
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/inventory"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load warehouse IDs
warehouses = []
with open(WAREHOUSE_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, start=1):
        warehouses.append(idx)  # deterministic IDs

print(f"Loaded {len(warehouses)} warehouses")

file_index = 1
row_count = 0
total_rows = 0

outfile = open(f'{OUTPUT_DIR}/inventory_batch_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerow(['product_id', 'warehouse_id', 'stock_quantity'])

for product_id in range(1, NUM_PRODUCTS + 1):
    for warehouse_id in warehouses:
        if row_count >= BATCH_SIZE:
            outfile.close()
            file_index += 1
            row_count = 0
            outfile = open(f'{OUTPUT_DIR}/inventory_batch_{file_index}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(outfile)
            writer.writerow(['product_id', 'warehouse_id', 'stock_quantity'])
        
        # realistic stock: high-demand categories higher, low-demand lower
        # example simplification: random weighted stock
        stock_quantity = random.choices(
            population=[0, random.randint(1,50), random.randint(51,200), random.randint(201,500)],
            weights=[5, 20, 50, 25],  # more medium-stock products
            k=1
        )[0]

        writer.writerow([product_id, warehouse_id, stock_quantity])
        row_count += 1
        total_rows += 1

outfile.close()
print(f"Inventory CSVs generated successfully in {OUTPUT_DIR} ({total_rows} rows total)")
