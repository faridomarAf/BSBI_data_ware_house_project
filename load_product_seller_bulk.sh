DB="EC_MARKETPLACE"
USER="root"
LOG="product_seller_load.log"

DATA_DIR="data/product_seller"
PROCESSED_DIR="$DATA_DIR/processed"
ERROR_DIR="$DATA_DIR/error"

export MYSQL_PWD='your sql password'

# Create directories if they don't exist
mkdir -p "$PROCESSED_DIR" "$ERROR_DIR"

echo "==== Load started at $(date) ====" >> $LOG

# Loop through all CSV files
for file in "$DATA_DIR"/product_seller_part_*.csv
do
  [ -e "$file" ] || continue  # Skip if no files

  echo "Loading $file ..." >> $LOG

  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Product_Seller
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, seller_id, supply_price);

COMMIT;
EOF

  if [ $? -eq 0 ]; then
    echo "SUCCESS: $file loaded" >> $LOG
    mv "$file" "$PROCESSED_DIR/"
  else
    echo "ERROR: $file failed" >> $LOG
    mv "$file" "$ERROR_DIR/"
  fi
done

echo "==== Load finished at $(date) ====" >> $LOG
