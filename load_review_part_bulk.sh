DB="EC_MARKETPLACE"
USER="root"
LOG="review_load.log"

DATA_DIR="data/reviews"
PROCESSED_DIR="$DATA_DIR/processed"
ERROR_DIR="$DATA_DIR/error"

export MYSQL_PWD='your sql password'

mkdir -p "$PROCESSED_DIR" "$ERROR_DIR"

echo "==== Load started at $(date) ====" >> $LOG

for file in "$DATA_DIR"/review_part_*.csv
do
  [ -e "$file" ] || continue

  echo "Loading $file ..." >> $LOG

  mysql --local-infile=1 -u $USER $DB <<EOF
START TRANSACTION;

SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE '$file'
INTO TABLE Review
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
  @review_id,
  product_id,
  customer_id,
  rating,
  comment,
  review_date
);

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;
EOF

  if [ $? -eq 0 ]; then
    mv "$file" "$PROCESSED_DIR/"
  else
    mv "$file" "$ERROR_DIR/"
  fi
done

echo "==== Load finished at $(date) ====" >> $LOG
