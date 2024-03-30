# Generated by Django 5.0.3 on 2024-03-30 18:31

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0005_alter_story_created_at_alter_story_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[400, 800], upload_to='stories'),
        ),
    ]
