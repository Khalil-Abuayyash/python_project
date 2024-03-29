# Generated by Django 2.2.4 on 2021-06-03 08:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_solved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='day', max_length=255)),
                ('algo', models.CharField(default='', max_length=255)),
                ('night_study', models.CharField(default='', max_length=255)),
                ('group_activity', models.CharField(default='', max_length=255)),
                ('discussion', models.CharField(default='', max_length=255)),
                ('lunch', models.CharField(default='', max_length=255)),
                ('date', models.DateField(default=datetime.datetime(2021, 6, 3, 11, 34, 18, 43160))),
            ],
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hardness', models.IntegerField()),
                ('code_review', models.TextField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
            ],
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('classes', models.ManyToManyField(through='student.Class', to='student.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('votes', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requstes', to='login.User')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(default=datetime.datetime(2021, 6, 3, 11, 34, 18, 52154))),
                ('end_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='student.Day')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to='login.User')),
                ('students', models.ManyToManyField(related_name='attended_events', to='login.User')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='student.EventCategory')),
            ],
        ),
        migrations.AddField(
            model_name='day',
            name='stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='student.Stack'),
        ),
        migrations.AddField(
            model_name='class',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Section'),
        ),
        migrations.AddField(
            model_name='class',
            name='stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Stack'),
        ),
        migrations.AddField(
            model_name='class',
            name='users',
            field=models.ManyToManyField(related_name='classes', to='login.User'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='student.Day'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='solvers',
            field=models.ManyToManyField(through='student.UserAssignment', to='login.User'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='student.Stack'),
        ),
    ]
