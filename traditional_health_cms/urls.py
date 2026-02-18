from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/user/', views.user_login, name='user_login'),
    path('login/creator/', views.creator_login, name='creator_login'),
    path('login/admin/', views.admin_login, name='admin_login'),

    path('ayurveda/', views.ayurveda, name='ayurveda'),
    path('yoga/', views.yoga, name='yoga'),
    path('remedies/', views.remedies, name='remedies'),
    path('food/', views.food, name='food'),
]
