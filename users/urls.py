from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('set_currency/', views.set_currency_view, name='set_currency'),
    path('buy_card/', views.buy_card, name='buy_card'),
    path('switch_role/<str:role>/', views.switch_role_view, name='switch_role'),
]
