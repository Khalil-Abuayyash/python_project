from django.db import models
# from django.contrib.auth import
from django.db.models.deletion import CASCADE
import bcrypt
import re


from django.db.models.fields.related import ForeignKey

class Role(models.Model):
    STUDENT = 1
    INSTRUCTOR = 2
    ROLE_CHOICES = (
      (STUDENT, 'student'),
      (INSTRUCTOR, 'instructor'),
    )
    type = models.IntegerField(default=0)
    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

class UserManger(models.Manager):
    def validator_registeration(self, postData):
        errors  = {}

        try:
            user = self.get(email=postData['email'])
            errors['exsited_email'] = f"{postData['email']} is already registered"
        except:
            pass
        
        if len(postData['first_name']) < 2 :
            errors['first_name'] = 'First name must be at least of two characters'

        if len(postData['last_name']) < 2 :
            errors['last_name'] = 'Last name must be at least of two characters'
        
        if len(postData['password']) < 8:
            errors['password'] = 'password must be at least of eight characters'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = 'invalid email address'
        
        # if postData['password'] != postData['confirm_password']:
        #     errors['password'] = 'password and coonfirm password are not the same'

        return errors
    def validator_login(self, postData):
        errors = {}
        try:
            user = self.get(email=postData['email'])

            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                pass
            else:
                errors['failed_password'] = "email and password are not matched"

        except:
            errors['existed_email'] = f"{postData['email']} is not registered"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255,default='')
    email = models.CharField(max_length=255,default='')
    password = models.CharField(max_length=255,default='')
    badge_id = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=255,default='')
    role = models.ForeignKey(Role, related_name='users', on_delete=CASCADE)
    absences = models.IntegerField(default=0)
    lates = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManger()

def create_student(postData):
    first_name = postData['first_name']
    last_name = postData['last_name']
    email = postData['email']
    password  = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
    badge_id =  postData['badge_id']
    phone_number =  postData['phone_number']
    role = Role.objects.get(id=Role.STUDENT)
    User.objects.create( 
                        first_name=first_name, last_name=last_name,email=email,
                        password=password, badge_id=badge_id, phone_number=phone_number, role=role
                        )
    return User.objects.last()

def create_instructor(postData):
    first_name = postData['first_name']
    last_name = postData['last_name']
    email = postData['email']
    password  = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
    badge_id =  postData['badge_id']
    phone_number =  postData['phone_number']
    role = Role.objects.get(id=Role.INSTRUCTOR)
    User.objects.create( 
                        first_name=first_name, last_name=last_name,email=email,
                        password=password, badge_id=badge_id, phone_number=phone_number, role=role
                        )
    return User.objects.last()

def get_user_details(email):
    try :
        user = User.objects.get(email=email)
        user.role.id
        if user.role.id == 1:
            role = 'student'
        elif user.role.id == 2:
            role = 'instructor'

        user_details = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'badge_id': user.badge_id,
            'phone_number': user.phone_number,
            'role': role
            # 'created_at': user.created_at,
            # 'updated_at': user.updated_at,
        }
    except:
        user_details= {}


    return user_details