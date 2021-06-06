from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('todo',views.to_do),
    path('<int:student_id>/edit_profile',views.show_update_user),
    path('<int:student_id>/update',views.update_user_info),
    path('choose_event',views.choose_event),
    path('requests',views.brackout_session),
    path('request_brackout',views.request_brackout),
    path('vote',views.vote),
    path('create_event',views.create_brackout),
    path('delete_request/<int:id>',views.delete_user_request),
    path('<int:student_id>/assignments',views.assignment),
    path('<int:student_id>/selected_assignment',views.selected_assignment),
    path('<int:student_id>/assignment_review',views.assignment_review),
    path('',views.students_progress),
    path('choose_students',views.choose_students),




    # path('<int:id>/edit', views.edit),
    url('header', views.header, name='header'),
    url('sidebar', views.sidebar, name='sidebar'),
]