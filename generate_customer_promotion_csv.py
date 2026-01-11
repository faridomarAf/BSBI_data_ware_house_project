import csv
import random
import os
from datetime import datetime, timedelta

NUM_CUSTOMERS = 9_000_000
NUM_PROMOTIONS = 50
MAX_PROMOS_PER_CUSTOMER = 3
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/customer_promotion"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file_index = 1
row_count = 0

outfile = open(f'{OUTPUT_DIR}/customer_promo_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerow(['customer_id', 'promotion_id', 'used_date'])

for customer_num in range(1, NUM_CUSTOMERS + 1):
    customer_id = f"DE-CUST-2024-{customer_num:09d}"
    promo_count = random.randint(0, MAX_PROMOS_PER_CUSTOMER)
    promos = random.sample(range(1, NUM_PROMOTIONS + 1), promo_count)

    for promo_id in promos:
        if row_count >= BATCH_SIZE:
            outfile.close()
            file_index += 1
            row_count = 0
            outfile = open(f'{OUTPUT_DIR}/customer_promo_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(outfile)
            writer.writerow(['customer_id', 'promotion_id', 'used_date'])

        used_date = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([customer_id, promo_id, used_date])
        row_count += 1

outfile.close()
print(f"Generated customer promotions in {file_index} files.")
