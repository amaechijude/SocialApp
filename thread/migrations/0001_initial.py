# Generated by Django 5.0.6 on 2024-08-20 10:35

import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=150)),
                ('user', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.IntegerField()),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id_user', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('bio', models.TextField(blank=True, max_length=1000)),
                ('profile_pics', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[1920, 1080], upload_to='profile_images')),
                ('github_url', models.URLField(blank=True, max_length=300, validators=[django.core.validators.URLValidator()])),
                ('linkedin_url', models.URLField(blank=True, max_length=300, validators=[django.core.validators.URLValidator()])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('postID', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=300)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[1920, 1080], upload_to='profile_posts')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('num_of_likes', models.IntegerField(default=0)),
                ('num_of_comments', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thread.profile')),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thread.postmodel')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thread.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[1920, 1080], upload_to='stories')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thread.profile')),
            ],
            options={
                'verbose_name_plural': 'Stories',
            },
        ),
    ]
