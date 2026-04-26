from django.contrib import admin
from django.urls import path
from courses.api import api  # Import instance 'api' dari file api.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls), # Semua endpoint API akan diawali dengan /api/
]