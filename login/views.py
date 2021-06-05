from django.contrib.messages.api import error
from django.db import models
from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login.html')

def create_student(request):
    print(1)
    if request.method == "POST":
        print('post')
        if 'id' in request.session:
            request.session.clear()
        errors = models.User.objects.validator_registeration(request.POST)
        if len(errors) > 0 :
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else :
            print('creating')
            student = models.create_student(request.POST)
            request.session['id'] = student.id
            return redirect('/')
    return redirect('/')

def create_instructor(request):
    print(1)
    if request.method == "POST":
        print('post')
        if 'id' in request.session:
            request.session.clear()

        if request.POST['code'] == '100':
            print('right code')
            errors = models.User.objects.validator_registeration(request.POST)
            if len(errors) > 0 :
                print('errors')
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            else :
                instructor = models.create_instructor(request.POST)
                request.session['id'] = instructor.id
                return redirect('/')
    return redirect('/')
            
def logging_in(request):
    if request.method == "POST":
        errors = models.User.objects.validator_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user_details = models.get_user_details(request.POST['email'])
            for key, value in user_details.items():
                request.session[key] = value
            messages.success(request, "Logged in successfully")
            return redirect("/students/todo")

def logout(request):
    request.session.clear()
    return redirect('/')

