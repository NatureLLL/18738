# Generated by Django 2.1.1 on 2018-09-27 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20180927_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='owner',
            new_name='user',
        ),
    ]
