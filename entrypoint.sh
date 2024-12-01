#!/bin/sh

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py create_admin

# Run the Django development server
exec python manage.py runserver 0.0.0.0:8000