from django.urls import path

from superadmin.views import *

urlpatterns = [
    path('get_request_logs', get_request_logs, name='get_request_logs'),
    path('get_all_exceptions', get_all_exceptions, name='get_all_exceptions'),
    path('add_new_store', add_new_store, name='add_new_store'),
    path('get_all_stores', get_all_stores, name='get_all_stores'),
    path('edit_store', edit_store, name='edit_store'),
    path('delete_store', delete_store, name='delete_store'),
]
