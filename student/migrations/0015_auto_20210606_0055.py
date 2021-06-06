# Generated by Django 2.2.4 on 2021-06-05 21:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_auto_20210605_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassignment',
            name='is_solved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 6, 0, 55, 38, 214045)),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 6, 0, 55, 38, 229680)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 6, 0, 55, 38, 229680)),
        ),
    ]