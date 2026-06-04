from django.urls import path
from . import views

app_name = 'promocodes'

urlpatterns = [
    path('list/', views.promo_list, name='list'),
]
