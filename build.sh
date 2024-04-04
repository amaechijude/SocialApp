#!/bin/bash
pip install -r requirements.txt
python manage.py makemigrations thread
python manage.py migrate