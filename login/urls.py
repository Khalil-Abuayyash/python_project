from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logging', views.logging_in),
    path('logging_out',views.logout),
    path('create_student', views.create_student),
    path('create_instructor', views.create_instructor),
]