from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('list/', views.review_list, name='list'),
    path('add/', views.add_review, name='add'),
]
