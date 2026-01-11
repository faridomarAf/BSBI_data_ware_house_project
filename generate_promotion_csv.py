import csv
import random
import string
import os

NUM_PROMOTIONS = 500  # increased for realistic DW
OUTPUT_DIR = "data/promotion"
os.makedirs(OUTPUT_DIR, exist_ok=True)

filename = f"{OUTPUT_DIR}/promotion.csv"

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['promo_code', 'discount_percent'])

    for _ in range(NUM_PROMOTIONS):
        # Promo code with prefix
        code = 'PROMO-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        discount = random.randint(5, 50)
        writer.writerow([code, discount])

print(f"Generated {filename}")
