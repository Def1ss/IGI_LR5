from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('sessions/', views.session_list, name='session_list'),
    path('enroll_group/<int:group_id>/', views.enroll_group, name='enroll_group'),
    path('schedule_session/', views.schedule_session, name='schedule_session'),
]
