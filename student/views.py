from django.shortcuts import render,redirect
from student.models import *
from login.models import *
import bcrypt
from django.contrib import messages
from datetime import datetime

# # Create your views here.
# def index(request):
#     return render(request, 'home.html')

# def header(request):
#     return render(request, 'header.html')

# def sidebar(request):
#     return render(request, 'sidebar.html')

# def edit(request, id):
#     return render(request, 'edit_profile.html')

#************************************************************************************************
# Home page - to do page
def to_do(request):
    today = Day.objects.get(date=datetime.today()) #make suer from the format from the models and today() they should match
    # if not match we can use
    # settings.py set DATE_INPUT_FORMATS 
    # DATE_INPUT_FORMATS = ['%d-%m-%Y']
    today_events = Event.objects.filter(date=datetime.today())
    print(today)
    context = {
        "today": today,
        # "Event": Event.objects.filter(date=datetime.today()), #today.events.all(),
        "user_events": user_event(request.session["id"]),
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
        return redirect("/students/edit")
    else:
        errors = {}
        errors['password'] = "password does not match"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/students/edit")

def choose_event(request):
    event_id = int(request.POST["event_id"])
    choose_events(request.session["id"],event_id)
    return redirect("todo")

#************************************************************************************************
# Home page - request page

def brackout_session(request):
    all_event = Event.objects.all()
    context = {
        "user": User.objects.get(id=request.seesion["id"]),
        "request":Request.objects.all(),
        "brackout": Request.objects.all(),
        "all_event": Event.objects.all()
            }
    return render(request,"request_brackout_Tamara.html",context)# /request

# the below 2 function is for the students to request an event and vote for one
def request_brackout(request):
    create_request(request.POST,request.session["id"])
    return redirect("requests")

def vote(request):
    selected_request = Request.objects.get(id=int(request.post["request"]))
    selected_request.votes += 1
    selected_request.save()
    return redirect("requests")

# the below 2 function is for the intructor to create an event and delete a request 
def create_brackout(request):
    create_Event(request.POST,request.session["id"])
    return redirect("/request")

def delete_user_request(request,id):
    delete_request(id)
    return redirect("/request")

#************************************************************************************************
# Home page - assignment page

def assignment(request,id):
    
    day = Day.objects.get(date=datetime.today())
    if 'day' in request.POST:
        day = Day.objects.get(name=request.POST['day'], stack=day.stack)

    stack = day.stack
    user = User.objects.get(id=id)
    c = Class.objects.get(user=user,stack=stack)
    section = c.section # it will be one section can i reach it without all()
    selected_satck = Stack.objects.get(name=request.session["selected_stack"])
    selected_assignment = Assignment.objects.get(name=request.POST["assignment"])
    assignments =  day.assignments.all()
    assignment_dict={}
    for assignment in assignments:
        assignment_dict[assignment] = UserAssignment.objects.get(user=user, assignment=assignment)

    context = {
        'selected_day': day,
        "stack_days": Stack.days.all(),
        "section": section,
        "stacks": Stack.objects.all(),
        'assignment_dict': assignment_dict,
        # "assignments": selected_satck.assignments.all(),
        # "selected_assignment":selected_assignment,
        "range":range(1,11)
    }
    return render(request,"assigment_Tamara.html",context)

def selected_assignment(request):
    request.session["selected_stack"] = request.POST["stack"]
    return redirect(str(request.session["di"])+"/assignments")

def assignment_review(request):
    create_userAssignment(request.POST,request.session["id"])
    return redirect(str(request.session["di"])+"/assignments")






