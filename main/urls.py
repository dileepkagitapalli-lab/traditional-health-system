from django.urls import path
from . import views

urlpatterns = [
    # Static pages
    path('', views.home, name='home'),
    path('ayurveda/', views.ayurveda, name='ayurveda'),
    path('yoga/', views.yoga, name='yoga'),
    path('remedies/', views.remedies, name='remedies'),
    path('food/', views.food, name='food'),

    # Auth
    path('login/user/', views.user_login, name='user_login'),
    path('login/creator/', views.creator_login, name='creator_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/user/', views.user_register, name='user_register'),
    path('register/creator/', views.creator_register, name='creator_register'),
    path('register/admin/', views.admin_register, name='admin_register'),

    # Dashboards
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/creator/', views.creator_dashboard, name='creator_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # Content actions
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/save/', views.save_post, name='save_post'),
    
    # Admin actions
    path('admin/post/<int:post_id>/approve/', views.approve_post, name='approve_post'),
    path('admin/post/<int:post_id>/reject/', views.reject_post, name='reject_post'),
]
