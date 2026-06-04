from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('dictionary/', views.term_list, name='term_list'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('faq/', views.faq_view, name='faq'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('dictionary/create/', views.term_create, name='term_create'),
    path('dictionary/<int:pk>/edit/', views.term_edit, name='term_edit'),
    path('dictionary/<int:pk>/delete/', views.term_delete, name='term_delete'),
    path("statistics/", views.statistics_page, name="statistics"),
    path("statistics/chart/", views.statistics_chart, name="statistics_chart"),
]
