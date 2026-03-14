from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Default Admin
    path('admin/', admin.site.urls),

    # Main App URLs
    path('', include('main.urls')),
]