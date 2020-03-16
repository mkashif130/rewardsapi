from django.urls import path

from public.views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('get_qr_code_of_store', get_qr_code_of_store, name='get_qr_code_of_store'),
]
