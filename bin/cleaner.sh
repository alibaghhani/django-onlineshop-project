#! /usr/bin/env bash

rm -rf db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --email admin@gmail.com --admin_name admin
