from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('<int:id>/edit', views.edit),
    url('header', views.header, name='header'),
    url('sidebar', views.sidebar, name='sidebar'),
]