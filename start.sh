#!/bin/bash

echo "Running database migrations..."
alembic upgrade head

echo "Running sql script..."
PGPASSWORD=$DB_PASS psql -h db -U $DB_USER -d $DB_NAME -f /app/initial_data.sql

echo "Starting application..."
exec python main.py