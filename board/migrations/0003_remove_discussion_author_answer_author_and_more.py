# Generated by Django 4.0.2 on 2022-02-04 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_alter_answer_id_alter_discussion_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='author',
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(default='exit', on_delete=django.db.models.deletion.CASCADE, related_name='author_answer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discussion',
            name='voter',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
