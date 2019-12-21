from django.urls import path

from public.views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard')
]
