DB="EC_MARKETPLACE"
USER="root"
LOG="payment_load.log"

DATA_DIR="data/payments"
PROCESSED_DIR="$DATA_DIR/processed"
ERROR_DIR="$DATA_DIR/error"

export MYSQL_PWD='your sql password'

# Ensure directories exist
mkdir -p "$PROCESSED_DIR" "$ERROR_DIR"

echo "==== Load started at $(date) ====" >> $LOG

# Loop through all payment CSV files
for file in "$DATA_DIR"/payment_part_*.csv
do
  [ -e "$file" ] || continue  # Skip if no files

  echo "Loading $file ..." >> $LOG

  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Payment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, amount, payment_method, payment_status, payment_date);

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
