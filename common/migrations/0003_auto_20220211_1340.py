# Generated by Django 3.1.3 on 2022-02-11 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_profile_username_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='USERNAME_FIELD',
        ),
    ]
