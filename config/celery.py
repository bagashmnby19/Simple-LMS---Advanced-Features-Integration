import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('healthylife_project')

# Menggunakan string di sini agar worker tidak perlu menserialisasikan objek konfigurasi
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task dari semua app Django yang terdaftar
app.autodiscover_tasks()