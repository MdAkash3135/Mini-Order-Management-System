#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "Postgres started"

# Run migrations
python manage.py migrate

# Collect static files (optional)
# python manage.py collectstatic --noinput

exec "$@"
