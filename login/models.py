from django.db import models
# from django.contrib.auth import
from django.db.models.deletion import CASCADE


from django.db.models.fields.related import ForeignKey

class Role(models.Model):
    type = models.IntegerField()

class User(models.Model):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255,default='')
    email = models.CharField(max_length=255,default='')
    password = models.CharField(max_length=255,default='')
    badge_id = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=255,default='')
    role = models.ForeignKey(Role, related_name='users', on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
