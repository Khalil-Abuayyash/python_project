from django.shortcuts import render,redirect
from student.models import *
from login.models import *
import bcrypt
from django.contrib import messages
from datetime import datetime
from django.contrib import messages
import json
from django.http import Http404, HttpResponse

# # Create your views here.
# def index(request):
#     return render(request, 'home.html')

def header(request):
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

def sidebar(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
    }
    return render(request, 'sidebar.html', context)


# def edit(request, id):
#     return render(request, 'edit_profile.html')

#************************************************************************************************
# Home page - to do page
def to_do(request):
    if 'id' not in request.session:
        return redirect('/')
    try :
        today = Day.objects.get(date=datetime.today()) 
    except:
        today = Day.objects.last()
    # if not match we can use
    # settings.py set DATE_INPUT_FORMATS 
    # DATE_INPUT_FORMATS = ['%d-%m-%Y']
    # today_events = Event.objects.filter(date=datetime.today())
    print(today)
    context = {
        'user': User.objects.get(id=request.session['id']),
        "today": today,
        "events": Event.objects.filter(date=today.date),
        # 'events': Event.objects.all()
        # "user_events": user_event(request.session["id"],today),
    }
    return render(request,"home.html",context)

def show_update_user(request, student_id):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=student_id)
    }
    return render(request, "edit_profile.html", context)

def update_user_info(request, student_id):
    
    if request.method == 'POST':
        if request.POST['pass'] == 'no':
            update_user(request.POST, student_id)
        else:
            if request.POST["password"] == request.POST["confirm_password"]:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                update_user(request.POST, student_id, password=pw_hash)
        return redirect(f'/students/{student_id}/edit_profile')
    return redirect("/students/todo")


def choose_event(request):
    if request.method == 'POST':
        event_id = request.POST["event_id"]
        choose_events(request.session["id"],event_id)
        return redirect("/students/todo")
    return redirect("/students/todo")

#************************************************************************************************
# Home page - request page

def brackout_session(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session["id"]),
        "requests":Request.objects.all(),
        # "brackout": Request.objects.all(),
        # "all_event": Event.objects.all()
        # 'range': [1,2,3,4,5]
        }
    return render(request,"requests.html",context)# /request

# the below 2 function is for the students to request an event and vote for one
def request_breakout(request):
    if request.method == 'POST':
        create_request(request.POST,request.session["id"])
        return redirect("/students/requests")
    return redirect("/students/todo")

def vote(request, request_id):
    if 'id' not in request.session:
        return redirect('/')
    selected_request = Request.objects.get(id=request_id)
    selected_request.votes += 1
    selected_request.save() 
    return redirect("/students/requests")

# the below 2 function is for the intructor to create an event and delete a request 
def create_breakout(request):
    if request.method == 'POST':
        create_Event(request.POST,request.session["id"])
        return redirect("/students/requests")
    return redirect("/students/todo")

def delete_user_request(request,id):
    if 'id' not in request.session:
        return redirect('/')
    delete_request(id)
    return redirect("/students/requests")

#************************************************************************************************
# Home page - assignment page
#the below 3 function is for the user to display their assigments and rate them
def assignment(request,student_id):
    if 'id' not in request.session:
        return redirect('/')
    request.session["student_id"] = student_id
    try :
        day = Day.objects.get(date=datetime.today())
    except:
        day = Day.objects.last()
    if 'day' in request.POST:
        day = Day.objects.get(name=request.POST['day'], stack=day.stack)

    if 'selected_stack' in request.session:
        stack = request.session['selected_stack']
    else :
        stack = day.stack
        
    user = User.objects.get(id=student_id)
    section = Section.objects.last()
    try :
        c = Class.objects.get(users=user,stack=stack)
    except:
        c = Class.objects.create(stack=stack,section=section)
        c.users.add(user)
    section = c.section # it will be one section can i reach it without all()
    # selected_satck = Stack.objects.get(name=request.session["selected_stack"])
    # selected_assignment = Assignment.objects.get(name=request.POST["assignment"])
    assignments =  day.assignments.all()
    assignment_dict={}
    try :
        for assignment in assignments:
            assignment_dict[assignment] = UserAssignment.objects.get(user=user, assignment=assignment)
    except:
        for assignment in assignments:
            assignment_dict[assignment] = 0
    

    context = {
        'selected_day': day,
        # 'selected_stack': stack,
        "stack_days": stack.days.all(),
        "section": section,
        'stack': stack,
        "stacks": Stack.objects.all(),
        'assignment_dict': assignment_dict,
        # 'assignment_dict': {
        #     1:'werw',
        #     2:'sdfsdf',
        #     3:'asdasd,'
        # },
        # "assignments": selected_satck.assignments.all(),
        # "selected_assignment":selected_assignment,
        "range":range(1,11),
        "current_user": User.objects.get(id=request.session["id"]),
        "selected_student": user,
        'student_id': student_id,
    }
    return render(request,"assignment.html",context)

def selected_assignment(request, student_id):# we might use ajax for this
    if 'id' not in request.session:
        return redirect('/')
    if 'selected_stack' in request.session:
        request.session["selected_stack"] = request.POST["stack"]
    # if request.session['role'] == 'instructor':
    #     return redirect(str(request.session["id"])+"/assignments")
    # if request.session['role'] == 'student':
    #     return redirect(str(request.session["id"])+"/assignments")
    return redirect(f"/students/{student_id}/assignments")


def assignment_review(request, student_id):
    if request.method == 'POST':
        errors = create_userAssignment(request.POST, student_id)
        request.session['assignment_id'] = request.POST['assignment_id']
        if len(errors) > 0 :
            for key,value in errors.items():
                messages.error(request, value)
        else:
            messages.success(request, "Code Review has been submitted successfully")
        return redirect(f"/students/{student_id}/assignments")
    return redirect("/students/todo")

#the below 3 function is for the instructer to display students assignments
def students_progress(request):
    if 'id' not in request.session:
        return redirect('/')
    if 'stack_id' in request.session and 'section_id' in request.session:
        selected_students = student_list(request.session["stack_id"],request.session["section_id"])
    else:
        selected_students = [0,0,0,0,0,0,0,0,0,0]

    context = {
        "stacks":Stack.objects.all(),
        "sections":Section.objects.all(),
        "selected_students": selected_students,
        }
    return render(request,"students_progress.html",context)

def choose_students(request):
    if request.method == 'POST':
        request.session["stack_id"] = request.POST["stack_id"]
        request.session["section_id"] = request.POST["section_id"]
        # student_list(request.POST["stack"],request.POST["section"])
        return redirect('/students')
    return redirect("/students/todo")
    
def vote_ajax(request):
    if request.is_ajax():
        khalil = ['khalil', 'abuayyash']
        data = json.dumps(khalil)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404





