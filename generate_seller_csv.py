import csv
import os
import random
import unicodedata
from faker import Faker

fake = Faker("de_DE")

# ---------------- CONFIG ----------------
NUM_SELLERS = 100_000
BATCH_SIZE = 50_000
OUTPUT_DIR = "data/seller"

EMAIL_DOMAINS = ["gmail.com", "web.de", "gmx.de", "outlook.com"]

os.makedirs(OUTPUT_DIR, exist_ok=True)

num_batches = (NUM_SELLERS + BATCH_SIZE - 1) // BATCH_SIZE
seller_counter = 1

def normalize(text: str) -> str:
    """Convert to safe ASCII for emails"""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return text.lower().replace(" ", "").replace("&", "and")

# ---------------------------------------
for batch in range(num_batches):
    filename = f"{OUTPUT_DIR}/seller_part_{batch+1:03}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["seller_name", "email"])

        rows_in_batch = min(BATCH_SIZE, NUM_SELLERS - seller_counter + 1)

        for _ in range(rows_in_batch):
            company_name = fake.company()
            domain = random.choice(EMAIL_DOMAINS)

            safe_name = normalize(company_name)
            email = f"{safe_name}.{seller_counter}@{domain}"

            writer.writerow([company_name, email])
            seller_counter += 1

    print(f"Generated {filename}")
