# Generated by Django 5.0.1 on 2024-02-29 06:54

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0005_alter_profile_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[300, 300], upload_to='profile_posts'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pics',
            field=django_resized.forms.ResizedImageField(crop=None, default='anon.png', force_format=None, keep_meta=True, quality=70, scale=None, size=[300, 300], upload_to='profile_images'),
        ),
    ]