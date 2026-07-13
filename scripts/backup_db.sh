#!/bin/bash
# اسکریپت بکاپ دیتابیس PostgreSQL
set -e

BACKUP_DIR=${BACKUP_DIR:-./backups}
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILE="$BACKUP_DIR/newmoonhome_$TIMESTAMP.sql"

pg_dump -h ${POSTGRES_HOST:-127.0.0.1} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres} ${POSTGRES_DB:-newmoonhome} > "$FILE"
echo "Backup saved to $FILE"
