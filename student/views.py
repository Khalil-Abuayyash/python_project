from django.shortcuts import render,redirect
from student.models import *
from login.models import *
import bcrypt
from django.contrib import messages
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'home.html')

def header(request):
    return render(request, 'header.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def edit(request, id):
    return render(request, 'edit_profile.html')


def home(request):
    today = Day.objects.get(date=datetime.today())
    context = {
        "today": today,
        "Event": Event.objects.filter(date=datetime.today()) #today.events.all()
    }
    return render(request,"To_do_Tamara.html",context)

def show_update_user(request):
    return render(request, "update.html")

def update_user_info(request):
    id = request.session["id"]
    if request.POST["password"] == request.POST["confirm_password"]:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        update_user(request.POST,id,pw_hash)
        return redirect("/update_user")
    else:
        errors = {}
        errors['password'] = "password does not match"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/update_user")

def assignment(request):
    today = Day.objects.get(date=datetime.today())
    section = today.stack.classes.section
    selected_satck = Stack.objects.get(name=request.POST["stack"])
    selected_assignment = Assignment.objects.get(name=request.POST["assignment"])
    context = {
        "day": Day.objects.all(),
        "section": section,
        "stack": Stack.objects.all(),
        "assignment": selected_satck.assignments.all(),
        "selected_assignment":selected_assignment,
        "range":range(1,11)
    }
    return render(request,"assigment_Tamara.html",context)

def assignment_add_data(request):
    create_userAssignment(request.POST,request.session["id"])
    return redirect("/assignment")

def brackout_session(request):
    context = {
        "request":Request.objects.all(),
        "user": User.objects.get(id=request.seesion["id"]),
        "brackout": Request.objects.all(),
            }
    return render(request,"request_brackout_Tamara.html",context)# /request

def request_brackout(request):
    create_request(request,request.session["id"])
    return redirect("/show_request")

def vote(request):
    selected_request = Request.objects.get(id=int(request.post["request"]))
    int(selected_request.votes) += 1
    selected_request.save()
    return redirect("/show_request")

def create_brackout(request):
    create_Event(request.POST,request.session["id"])
    return redirect("/request")

def delete(request,id):
    delete_request(id)
    return redirect("/request")






