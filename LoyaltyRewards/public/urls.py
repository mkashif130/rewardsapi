from django.urls import path

from public.views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('get_qr_code_of_user', get_qr_code_of_user, name='get_qr_code_of_user'),
    path('get_store_offers', get_store_offers, name='get_store_offers'),
]
