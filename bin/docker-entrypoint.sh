#!/bin/bash
echo "Launching...."
# Collect static files
echo "Collect static files"
# python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
exec gunicorn meshhairline.wsgi:application --timeout 300 --bind 0.0.0.0:8080