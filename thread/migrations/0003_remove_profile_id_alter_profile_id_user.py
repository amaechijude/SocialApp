# Generated by Django 4.2.7 on 2024-02-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0002_profile_first_name_profile_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AlterField(
            model_name='profile',
            name='id_user',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
