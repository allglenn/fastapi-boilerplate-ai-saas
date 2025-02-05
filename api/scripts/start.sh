#!/bin/bash
set -e

# Change to the app directory
cd /app

# Add the current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/app

# Wait for the database to be ready
echo "Waiting for database to be ready..."
python -m scripts.wait_for_db

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
exec "$@" 