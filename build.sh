#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations thread
python manage.py migrate