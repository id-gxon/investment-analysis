# Generated by Django 3.1.3 on 2022-02-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20220211_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
