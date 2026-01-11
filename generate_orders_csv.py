import csv
import random
import os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('de_DE')

NUM_CUSTOMERS = 9_000_000
MAX_ORDERS_PER_CUSTOMER = 5
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/orders"
os.makedirs(OUTPUT_DIR, exist_ok=True)

order_id = 1
file_index = 1
row_count = 0

status_weights = [
    ('Delivered', 70),
    ('Shipped', 15),
    ('Pending', 10),
    ('Cancelled', 5)
]

def weighted_status():
    return random.choices(
        [s for s, _ in status_weights],
        weights=[w for _, w in status_weights],
        k=1
    )[0]

file = open(f'{OUTPUT_DIR}/orders_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['order_id', 'customer_id', 'order_date', 'order_status'])

for customer_num in range(1, NUM_CUSTOMERS + 1):
    customer_id = f"DE-CUST-2024-{customer_num:09d}"
    orders_count = random.randint(0, MAX_ORDERS_PER_CUSTOMER)

    for _ in range(orders_count):
        if row_count >= BATCH_SIZE:
            file.close()
            file_index += 1
            row_count = 0
            file = open(f'{OUTPUT_DIR}/orders_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(file)
            writer.writerow(['order_id', 'customer_id', 'order_date', 'order_status'])

        order_date = fake.date_time_between(start_date='-2y', end_date='now').strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([order_id, customer_id, order_date, weighted_status()])
        order_id += 1
        row_count += 1

file.close()
print(f"Generated {order_id - 1} orders across {file_index} files.")
