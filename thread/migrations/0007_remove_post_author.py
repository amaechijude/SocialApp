# Generated by Django 4.2.7 on 2024-02-04 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0006_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
