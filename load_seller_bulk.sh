DB="EC_MARKETPLACE"
USER="root"
LOG="seller_load.log"

SELLER_DIR="data/seller"
PROCESSED="$SELLER_DIR/processed"
ERROR="$SELLER_DIR/error"

export MYSQL_PWD='your sql password'

mkdir -p "$PROCESSED" "$ERROR"

echo "==== Seller load started at $(date) ====" >> $LOG

for file in $SELLER_DIR/seller_part_*.csv
do
  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Seller
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(seller_name, email);

COMMIT;
EOF

  if [ $? -eq 0 ]; then
    mv "$file" "$PROCESSED/"
    echo "SUCCESS: $file" >> $LOG
  else
    mv "$file" "$ERROR/"
    echo "ERROR: $file" >> $LOG
  fi
done

echo "==== Seller load finished at $(date) ====" >> $LOG
