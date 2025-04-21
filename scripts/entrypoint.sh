#!/bin/bash
set -e

# Script for Docker entrypoint
# This script handles database migrations and other initialization tasks

# Wait for the database to be ready
echo "Waiting for database..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is up - continuing"

# Apply database migrations
echo "Applying database migrations..."
python -c "from app import db; db.create_all()"
echo "Migrations applied"

# Create log directory if it doesn't exist
mkdir -p /app/logs

# Execute command
echo "Starting application with command: $@"
exec "$@"