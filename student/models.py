from django.db import models
from django.db.models.fields.related import ForeignKey
from login.models import *

class Request(models.Model):
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='requstes', on_delete=CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

class Section(models.Model):
    name = models.CharField(max_length=255)

class Stack(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    classes = models.ManyToManyField(
        Section,
        through='Class',
        through_fields=('stack', 'section')
    )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

class Class(models.Model):
    stack = models.ForeignKey(Stack, on_delete=CASCADE)
    section = models.ForeignKey(Section, on_delete=CASCADE)
    users = models.ManyToManyField(User, related_name='classes')
    progress = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Assignment(models.Model):
    name = models.CharField(max_length=255)
    is_solved = models.BooleanField(default=False)
    stack = models.ForeignKey(Stack, related_name='assignments', on_delete=CASCADE)
    solvers = models.ManyToManyField(
        User,
        through='UserAssignment',
        through_fields=('assignment' ,'user' ),
    )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

class UserAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    hardness = models.IntegerField()
    code_review = models.TextField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #should we use the by who action

class EventCategory(models.Model):
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    type = models.ForeignKey(EventCategory, related_name='events', on_delete=CASCADE)
    instructor = models.ForeignKey(User, related_name='created_events', on_delete=CASCADE)
    students = models.ManyToManyField(User, related_name='attended_events')
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


