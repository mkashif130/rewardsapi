from django.urls import path

from registration.views import *

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('sign_up', sign_up, name='sign_up'),
    path('activate_account', activate_account, name='activate_account'),
]
