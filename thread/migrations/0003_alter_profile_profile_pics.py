# Generated by Django 4.2.7 on 2024-01-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0002_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pics',
            field=models.ImageField(default='anon.jpg', upload_to='profile_images'),
        ),
    ]
