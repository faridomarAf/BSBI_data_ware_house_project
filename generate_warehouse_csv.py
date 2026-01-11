import csv
import os

warehouses = ['Berlin Central', 'Munich North', 'Hamburg East', 'Frankfurt West', 'Cologne South']

OUTPUT_DIR = "data/warehouse"
os.makedirs(OUTPUT_DIR, exist_ok=True)

filename = f"{OUTPUT_DIR}/warehouse.csv"

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['location'])
    for loc in warehouses:
        writer.writerow([loc])

print(f"Generated {filename}")
