# Generated by Django 2.2.4 on 2021-06-05 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20210604_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='absences',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='lates',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
