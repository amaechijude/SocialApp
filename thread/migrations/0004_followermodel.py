# Generated by Django 5.0.1 on 2024-02-11 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0003_alter_likepost_postid'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
