DB="EC_MARKETPLACE"
USER="root"
LOG="orders_load.log"

DATA_DIR="data/orders"
PROCESSED_DIR="$DATA_DIR/processed"
ERROR_DIR="$DATA_DIR/error"

export MYSQL_PWD='your sql password'

# Ensure directories exist
mkdir -p "$PROCESSED_DIR" "$ERROR_DIR"

echo "==== Load started at $(date) ====" >> $LOG

# Loop through all orders CSV files
for file in "$DATA_DIR"/orders_part_*.csv
do
  [ -e "$file" ] || continue  # Skip if no files

  echo "Loading $file ..." >> $LOG

  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, order_date, order_status);

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
