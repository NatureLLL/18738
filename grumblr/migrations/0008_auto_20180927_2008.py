# Generated by Django 2.1.1 on 2018-09-27 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_auto_20180927_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='fist_name',
            new_name='first_name',
        ),
    ]