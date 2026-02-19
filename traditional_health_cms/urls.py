from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-login/', views.user_login, name='user_login'),
    path('creator-login/', views.creator_login, name='creator_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('ayurveda/', views.ayurveda, name='ayurveda'),
    path('yoga/', views.yoga, name='yoga'),
    path('remedies/', views.remedies, name='remedies'),
    path('food/', views.food, name='food'),
]
