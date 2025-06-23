#!/bin/bash
set -e

BACKUP_FILE="./backup/backup.sql"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "No backup file found"
  exit 0
fi

if [[ "$BACKUP_FILE" == *.dump ]] || [[ "$BACKUP_FILE" == *.custom ]]; then
  echo "Restoring binary dump..."
  PGPASSWORD=$DB_PASS pg_restore -h postgres -U $DB_USER -d $DB_NAME -j 4 --clean --if-exists "$BACKUP_FILE"
elif [[ "$BACKUP_FILE" == *.sql ]] || [[ "$BACKUP_FILE" == *.txt ]]; then
  echo "Restoring SQL dump..."
  PGPASSWORD=$DB_PASS psql -h postgres -U $DB_USER -d $DB_NAME -f "$BACKUP_FILE"
else
  echo "Unknown backup format. Supported extensions: .sql, .txt, .dump, .custom"
  exit 1
fi

echo "Restore completed successfully"