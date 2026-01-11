DB="EC_MARKETPLACE"
USER="root"
LOG="warehouse_load.log"

DATA_DIR="data/warehouse"
PROCESSED_DIR="$DATA_DIR/processed"
ERROR_DIR="$DATA_DIR/error"

export MYSQL_PWD='your sql password'

mkdir -p "$PROCESSED_DIR" "$ERROR_DIR"

echo "==== Load started at $(date) ====" >> $LOG

for file in "$DATA_DIR"/warehouse*.csv
do
  [ -e "$file" ] || continue

  echo "Loading $file ..." >> $LOG

  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Warehouse
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(location);

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
