# Generated by Django 2.2.4 on 2021-06-03 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 13, 46, 31, 819675)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 3, 13, 46, 31, 919958)),
        ),
    ]