from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home.html')

def header(request):
    return render(request, 'header.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def edit(request, id):
    return render(request, 'edit_profile.html')