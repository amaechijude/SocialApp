# Generated by Django 5.0.2 on 2024-04-03 14:59

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0013_alter_postmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=(256, 256), upload_to='profile_posts'),
        ),
    ]