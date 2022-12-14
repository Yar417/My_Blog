# Generated by Django 4.1.3 on 2022-11-20 07:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Статья', max_length=100, verbose_name='Название статьи')),
                ('text', models.TextField(verbose_name='Текст статьи')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 11, 20, 7, 32, 32, 287405, tzinfo=datetime.timezone.utc))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
