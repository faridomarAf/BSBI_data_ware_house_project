import csv
from faker import Faker
import os

fake = Faker('de_DE')

NUM_CUSTOMERS = 9_000_000
BATCH_SIZE = 100_000
OUTPUT_DIR = "data/customers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

num_batches = NUM_CUSTOMERS // BATCH_SIZE
if NUM_CUSTOMERS % BATCH_SIZE != 0:
    num_batches += 1

for batch in range(num_batches):
    filename = f"{OUTPUT_DIR}/customer_part_{batch+1}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['customer_id', 'first_name', 'last_name', 'email', 'phone', 'created_at'])

        for i in range(BATCH_SIZE):
            global_index = batch * BATCH_SIZE + i + 1
            if global_index > NUM_CUSTOMERS:
                break
            first = fake.first_name()
            last = fake.last_name()
            customer_id = f"DE-CUST-2024-{global_index:09d}"
            email = f"{first.lower()}.{last.lower()}.{global_index}@gmail.com"
            phone = fake.phone_number()
            created_at = fake.date_time_between(start_date='-2y', end_date='now').strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([customer_id, first, last, email, phone, created_at])

    fake.unique.clear()
print(f"Generated {NUM_CUSTOMERS} customers in {num_batches} files.")
