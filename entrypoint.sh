#!/bin/bash

# Wait for the database to be ready
echo "Applying database migrations..."
python manage.py migrate

# Start the Django application
echo "Starting Django application..."
python manage.py runserver 0.0.0.0:8000