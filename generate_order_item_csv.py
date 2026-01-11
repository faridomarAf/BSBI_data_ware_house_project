import csv
import random
import os

NUM_PRODUCTS = 100_000
LAST_ORDER_ID = 22_000_000  # replace with actual max order_id from Orders CSV
MAX_ITEMS_PER_ORDER = 5
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/order_items"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file_index = 1
row_count = 0

file = open(f'{OUTPUT_DIR}/order_item_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['order_id', 'product_id', 'quantity'])

for order_id in range(1, LAST_ORDER_ID + 1):

    items_count = random.randint(1, MAX_ITEMS_PER_ORDER)
    product_ids = random.sample(range(1, NUM_PRODUCTS + 1), items_count)

    for product_id in product_ids:

        if row_count >= BATCH_SIZE:
            file.close()
            file_index += 1
            row_count = 0
            file = open(f'{OUTPUT_DIR}/order_item_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(file)
            writer.writerow(['order_id', 'product_id', 'quantity'])

        # realistic quantity weighting: smaller quantities more common
        quantity = random.choices(
            population=[1,2,3,4,5,6,7,8,9,10],
            weights=[30,25,15,10,5,5,3,3,2,2],
            k=1
        )[0]

        writer.writerow([order_id, product_id, quantity])
        row_count += 1

file.close()
print(f"Order items generated in {file_index} files at {OUTPUT_DIR}")
