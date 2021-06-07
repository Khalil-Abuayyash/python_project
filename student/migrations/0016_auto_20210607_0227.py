# Generated by Django 2.2.4 on 2021-06-06 23:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_auto_20210606_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='progress',
            field=models.CharField(default='on pace', max_length=255),
        ),
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 7, 2, 27, 21, 420131)),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 7, 2, 27, 21, 435760)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 7, 2, 27, 21, 435760)),
        ),
    ]