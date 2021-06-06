from django.db import models
from django.db.models.fields.related import ForeignKey
from login.models import *
from datetime import datetime

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


class Day(models.Model):
    stack = models.ForeignKey(Stack, related_name='days', on_delete=CASCADE)
    name = models.CharField(max_length=255, default='day')
    algo = models.CharField(max_length=255, default='')
    night_study = models.CharField(max_length=255, default='')
    group_activity = models.CharField(max_length=255, default='')
    discussion = models.CharField(max_length=255, default='')
    lunch = models.CharField(max_length=255, default='')
    date = models.DateField(default=datetime.today())


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
    day = models.ForeignKey(Day, related_name='assignments', on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

class UserAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    hardness = models.IntegerField()
    is_solved = models.BooleanField(default=False)
    code_review = models.TextField(default='') # it will not filled by the user it will be blank when i get the user rating or coomplain from the assignment
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
    start_time = models.TimeField(default=datetime.now())
    end_time = models.TimeField(default=datetime.now())
    type = models.ForeignKey(EventCategory, related_name='events', on_delete=CASCADE)
    instructor = models.ForeignKey(User, related_name='created_events', on_delete=CASCADE)
    students = models.ManyToManyField(User, related_name='attended_events')
    day = models.ForeignKey(Day, related_name='events', on_delete=CASCADE)
    attend = models.CharField(max_length=255,default="optional")
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


def update_user(data,id,**kwargs):
    user = User.objects.get(id=id)

    if 'password' not in kwargs:
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.phone_number = data["phone_number"]
    else:
        user.password = kwargs['password']

    user.save()
    

def choose_events(id,event_id):
    user = User.objects.get(id=id)
    selected_event = user.attended_events.get(id=event_id)
    selected_event.attend = "mandatory"
    selected_event.save()

def user_event(id,day):
    user = User.objects.get(id=id)
    return user.attended_events.filter(date=day.date) #a date can have many events

def create_request(data,id):
    # we should have a type of valudation for the user in case he add an already existed suggition
    user = User.objects.get(id=id)
    Request.objects.create(desc=data["brackout"],user=user, votes=0)

def create_Event(data,id):
    instructor = User.objects.get(id=id)
    try :
        today = Day.objects.get(date=datetime.today())
    except:
        today = Day.objects.last()
    Event.objects.create(title=data["title"],date=data["date"],start_time=data["start_time"],end_time=data["end_time"],type=data["type"],instructor=instructor,day=today,attend=data["attend"])

def delete_request(id):
    selected_request = Request.objects.get(id=id)
    selected_request.delete()

def create_userAssignment(data,user_id):
    user = User.objects.get(id=user_id)
    assignment = Assignment.objects.get(id=data['assignment_id'])
    if "code_review" in data:
        user_assignment = UserAssignment.objects.get(assignment=assignment, user=user)
        user_assignment.code_review = data["code_review"]
        user_assignment.save()
    else:

        try :
            user_assignment = UserAssignment.objects.get(assignment=assignment, user=user)
            user_assignment.hardness = data["hardness"]
            user_assignment.comment = data["comment"]
            if "is_solved" in data:
                user_assignment.is_solved = True
            else:
                user_assignment.is_solved = False
            user_assignment.save()
        except:
            if "is_solved" in data:
                
                UserAssignment.objects.create(
                                assignment=assignment,user=user,hardness=data["hardness"],
                                comment=data["comment"], is_solved=True
                                )
            else:
                
                UserAssignment.objects.create(
                                    assignment=assignment,user=user,hardness=data["hardness"],
                                    comment=data["comment"], is_solved=False
                                    )

def student_list(stack_id,section_id):
    section = Section.objects.get(id=section_id)
    stack = Stack.objects.get(id=stack_id)
    selceted_class = Class.objects.get(stack=stack,section=section)
    return selceted_class.users.all()




