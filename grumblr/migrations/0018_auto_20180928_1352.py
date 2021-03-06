# Generated by Django 2.1.1 on 2018-09-28 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0017_auto_20180928_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='followings', to=settings.AUTH_USER_MODEL),
        ),
    ]
