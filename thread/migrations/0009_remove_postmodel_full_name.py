# Generated by Django 4.2.7 on 2024-03-04 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0008_postmodel_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmodel',
            name='full_name',
        ),
    ]
