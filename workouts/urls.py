from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('schedule/', views.schedule_view, name='schedule'),
    path('bulk_price/', views.bulk_price, name='bulk_price'),
    path('enroll_group/<int:group_id>/', views.enroll_group, name='enroll_group'),
]
