#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

SECRET_KEY=django-insecure-ob#0#_*$kyc*!i2l^o+&)r)q+9e3y02u1yk^##(uy3f$05ddm5

DEBUG=True

#DATABASE_URL=postgres://socialappdb_eq21_user:Dqfa3krxnAxtomWYGE0LxRvV5XVCHYgE@dpg-co215qgl6cac73d36q3g-a.oregon-postgres.render.com/socialappdb_eq21

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_USER=postgres.cymedfwbbqfscnbkmflw
DATABASE_NAME=postgres
DATABASE_PASSWORD=iI3kAT08E8y2R9Ks
DATABASE_HOST=aws-0-eu-central-1.pooler.supabase.com

CLOUD_NAME=dwroijswj
CLOUD_API_KEY=492888622693346
API_SECRET=jMVVFTAEJGk94PsmIq3o6er8kwU
CLOUD_SECURE=True
