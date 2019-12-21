# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

ROLES_ = tuple([(v, k) for k, v in settings.ROLES.items()])


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.IntegerField(blank=False, default=0, choices=ROLES_)
    name = models.TextField(default='')
    # 0 for male
    # 1 for female
    # 2 for other
    gender = models.IntegerField(default=0)
    dob = models.DateField(null=True)
    profile_image = models.TextField(default='')
    is_account_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)


class ForgotPasswordEmailKeys(models.Model):
    key = models.CharField(max_length=256, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_removed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now_add=True, null=True)


class AccountActivationKeys(models.Model):
    key = models.CharField(max_length=256, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_removed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now_add=True, null=True)


class UserSession(models.Model):
    user_id = models.ForeignKey(User, related_name='session_user_id', on_delete=models.CASCADE, null=True)
    device_id = models.TextField(default='')
    device_type = models.TextField(default='')
    user_agent = models.TextField(default='')
    # 0 for User
    user_type = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    fcm_token = models.TextField(null=True)
    fcm_token_active = models.BooleanField(default=False)
    login_time = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)


class LogEntryForException(models.Model):
    log_type = models.IntegerField(default=0)
    exception = models.TextField(default='')
    requested_url = models.TextField(default='', null=True)
    user_agent = models.TextField(default='', null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.exception


class SystemActivity(models.Model):
    log_type = models.IntegerField(default=1)
    message = models.TextField(default='', null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    requested_url = models.TextField(default='', null=True)
    user_agent = models.TextField(default='', null=True)
    access_token = models.TextField(default='', null=True)
    is_removed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now_add=True, null=True)


class LoggingOfEveryRequest(models.Model):
    is_authenticated_request = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    log_data = models.TextField(default='')
    created_on = models.IntegerField(default=0)
