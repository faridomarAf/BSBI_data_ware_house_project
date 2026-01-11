import csv
import random
import os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('de_DE')

NUM_CUSTOMERS = 9_000_000
NUM_PRODUCTS = 100_000
MAX_REVIEWS_PER_CUSTOMER = 3
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/reviews"
os.makedirs(OUTPUT_DIR, exist_ok=True)

review_id = 1
file_index = 1
row_count = 0

file = open(f'{OUTPUT_DIR}/review_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['review_id', 'product_id', 'customer_id', 'rating', 'comment', 'review_date'])

for customer_num in range(1, NUM_CUSTOMERS + 1):
    customer_id = f"DE-CUST-2024-{customer_num:09d}"
    review_count = random.randint(0, MAX_REVIEWS_PER_CUSTOMER)
    
    for _ in range(review_count):
        if row_count >= BATCH_SIZE:
            file.close()
            file_index += 1
            row_count = 0
            file = open(f'{OUTPUT_DIR}/review_part_{file_index}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(file)
            writer.writerow(['review_id', 'product_id', 'customer_id', 'rating', 'comment', 'review_date'])
        
        product_id = random.randint(1, NUM_PRODUCTS)
        rating = random.randint(1, 5)
        comment = fake.sentence(nb_words=12)
        review_date = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d %H:%M:%S")
        
        writer.writerow([review_id, product_id, customer_id, rating, comment, review_date])
        review_id += 1
        row_count += 1

file.close()
print(f"Generated reviews in {file_index} files, total reviews: {review_id-1}")
