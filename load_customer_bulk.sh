DB="EC_MARKETPLACE"
USER="root"
LOG="customer_load.log"

CUSTOMER_DIR="data/customers"
PROCESSED_DIR="$CUSTOMER_DIR/processed"
ERROR_DIR="$CUSTOMER_DIR/error"

export MYSQL_PWD='your sql password'

mkdir -p "$PROCESSED_DIR" "$ERROR_DIR"

echo "==== Customer load started at $(date) ====" >> $LOG

for file in $CUSTOMER_DIR/customer_part_*.csv
do
  echo "Loading $file ..." >> $LOG

  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Customer
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, first_name, last_name, email, phone, created_at);

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

echo "==== Customer load finished at $(date) ====" >> $LOG
