# Generated by Django 5.0.1 on 2024-03-24 06:18

import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0004_remove_story_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='content',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[1920, 1080], upload_to='profile_posts'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pics',
            field=django_resized.forms.ResizedImageField(crop=None, default='anon.png', force_format=None, keep_meta=True, quality=70, scale=None, size=[1920, 1080], upload_to='profile_images'),
        ),
    ]
