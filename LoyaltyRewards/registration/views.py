# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from LoyaltyRewards.decorators import *
from LoyaltyRewards.utils import *
from public.models import Public
from registration.models import *


def generate_auth_token(user_id, device_type, user_agent, user_type):
    login_time = datetime.datetime.now().timestamp()
    data_ = {'login_time': login_time, 'user_id': user_id}
    encoded_token = jwt.encode(data_, settings.SECRET_KEY_JWT, algorithm=settings.ALGORITHM_JWT)
    encoded_token = encoded_token.decode('utf-8')

    UserSession.objects.create(user_id_id=user_id, user_agent=user_agent, login_time=login_time,
                               user_type=user_type)
    return encoded_token


#
# def activate_account(request):
#     requested_url = request.META.get('HTTP_REFERER', None)
#     user_agent = request.META.get('HTTP_USER_AGENT', None)
#     try:
#         key = request.GET.get('key', '')
#         try:
#             try:
#                 account_activation_instance = AccountActivationKeys.objects.get(key=key)
#             except:
#                 context = {
#                     'description': 'This link has been expired or used'
#                 }
#                 return render(request, 'registration/activation-confirmation.html', context=context)
#
#             user = User.objects.get(id=account_activation_instance.user_id.id)
#             activate_user(user)
#
#             try:
#                 context = {
#                     'description': 'Congratulations!!! Your account has successfully activated!!'
#                 }
#                 text_content = render_to_string('registration/activation-confirmation.html', context)
#                 html_content = render_to_string('registration/activation-confirmation.html', context)
#
#                 email_instance = EmailMultiAlternatives('Welcome to Loyalty Rewards family', text_content)
#                 email_instance.attach_alternative(html_content, "text/html")
#                 email_instance.to = [user.username]
#                 email_instance.send()
#
#             except:
#                 pass
#
#             account_activation_instance.key = None
#             account_activation_instance.is_removed = True
#             account_activation_instance.save()
#
#             context = {
#                 'description': 'Congratulations!!! Your account has successfully activated!!'
#             }
#             return render(request, 'registration/activation-confirmation.html', context=context)
#
#         except:
#             context = {
#                 'description': 'This link has been expired or used'
#             }
#             return render(request, 'registration/activation-confirmation.html', context=context)
#
#     except Exception as e:
#         exception_log_entry(e, requested_url, user_agent)
#         context = {
#             'description': 'This link has been expired or used'
#         }
#         return render(request, 'registration/registration-confirmation.html', context=context)


@public_rest_call(['POST'])
def activate_account(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = json.loads(request.body.decode('utf-8'))
        key = data['key']
        try:
            account_activation_instance = AccountActivationKeys.objects.get(key=key)
        except:
            data = {"success": False}
            return {"data": data, "message": "This code has been expired or used", "status": BAD_REQUEST_CODE}

        user = User.objects.get(id=account_activation_instance.user_id.id)
        activate_user(user)

        account_activation_instance.key = None
        account_activation_instance.is_removed = True
        account_activation_instance.save()

        data = {"success": True}
        return {"data": data, "message": 'Congratulations!!! Your account has successfully activated!!',
                "status": SUCCESS_RESPONSE_CODE}

    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": 'Something went wrong', "status": BAD_REQUEST_CODE}


#
# @public_rest_call(['POST'])
# def resend_activation_code(request):
#     """
#     Reset account activation user to the user email address given in the user profile
#     :param request:
#     :return:
#     """
#     requested_url = request.META.get('HTTP_REFERER', None)
#     user_agent = request.META.get('HTTP_USER_AGENT', None)
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         email = data['email'].lower().strip()
#         user_object = User.objects.filter(username=email).last()
#         if not user_object.is_active:
#             ack = AccountActivationKeys.objects.filter(user_id=user_object, is_removed=False).last()
#             if ack:
#                 if ack.key != None:
#                     context = {
#                         'activation_code': str(ack.key),
#                         'LOGO_SOURCE': LOGO_SOURCE
#                     }
#                     try:
#                         text_content = render_to_string('utils/registration_confirmation.html', context)
#                         html_content = render_to_string('utils/registration_confirmation.html', context)
#                         email_instance = EmailMultiAlternatives('Account Activation', text_content)
#                         email_instance.attach_alternative(html_content, "text/html")
#                         email_instance.to = [email]
#                         email_instance.send()
#
#                     except Exception as e:
#                         exception_log_entry(e, requested_url, user_agent)
#
#                     data = {"success": True}
#                     return {"data": data, "message": "Email sent", "status": SUCCESS_RESPONSE_CODE}
#
#         data = {"success": False}
#         return {"data": data, "message": "Your account has already activated", "status": BAD_REQUEST_CODE}
#
#     except Exception as e:
#         exception_log_entry(e, requested_url, user_agent)
#         data = {"success": False}
#         return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@public_rest_call(['POST'])
def login(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['email']
        password = data['password']
        username = username.lower().strip()

        user = authenticate(username=username, password=password)
        if user is not None:
            # if user.is_active:
            if user.is_superuser:
                token = generate_auth_token(user.id, '', '', 1)
                data = {"access_token": token, "profile_info": {'name': user.first_name}}
                return {"data": data, "message": "Success", "status": SUCCESS_RESPONSE_CODE}
            else:
                # if Profile.objects.filter(user=user).exists():
                profile = Profile.objects.get(user=user)
                token = generate_auth_token(user.id, '', '', profile.role)
                profile_info = login_signup_info(profile)
                data = {"access_token": token, "profile_info": profile_info}
                if user.is_active:
                    is_active_user = True
                    message = "Success!!"
                else:
                    is_active_user = False
                    message = "Your account is not activated yet"
                data['is_active_user'] = is_active_user
                return {"data": data, "message": message, "status": SUCCESS_RESPONSE_CODE}
                # else:
                #     data = {"success": False}
                #     return {"data": data, "message": "Your account is not active yet", "status": BAD_REQUEST_CODE}
        else:
            data = {"success": False}
            return {"data": data, "message": "Incorrect email or password", "status": BAD_REQUEST_CODE}

    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": 'Something went wrong', "status": BAD_REQUEST_CODE}


@authenticated_rest_call(['GET', 'POST'])
def logout(request):
    """
    User logout View
    :param request:
    :return:
    """
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        token = request.META['HTTP_AUTHORIZATION']
        decoded_token = jwt.decode(token, settings.SECRET_KEY_JWT, algorithm=[settings.ALGORITHM_JWT])
        user_ = User.objects.get(id=int(decoded_token['user_id']))
        user_session = UserSession.objects.filter(user_id=user_, login_time=int(decoded_token['login_time']),
                                                  is_active=True).last()
        user_session.is_active = False
        user_session.fcm_token_active = False
        user_session.save()

        data = {"success": True}
        return {"data": data, "message": "Success", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


def generate_random_string(length):
    key = ''.join(random.choice(string.ascii_letters) for x in range(length))
    key = key
    return key


@public_rest_call(['POST'])
def sign_up(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'] if 'name' in data else ''
        contact_no = data['contact_no'] if 'contact_no' in data else ''

        if User.objects.filter(username=email).exists():
            data = {"success": False}
            return {"data": data, "message": "This email address is already registered", "status": BAD_REQUEST_CODE}
        else:
            user_object = User.objects.create(username=email, email=email)
            user_object.set_password(password)
            user_object.name = name
            user_object.is_active = False
            user_object.save()
            profile = Profile.objects.create(user=user_object, role=0, name=name)
            profile.contact_no = contact_no
            profile.save()
            Public.objects.create(profile=profile, name=name)

            while True:
                key = generate_random_string(10)
                if not AccountActivationKeys.objects.filter(key=key).exists():
                    break

            ack, created = AccountActivationKeys.objects.get_or_create(user_id=user_object)
            ack.key = key
            ack.save()

            context = {'url': key}

            text_content = render_to_string('registration/registration-confirmation.html', context)
            html_content = render_to_string('registration/registration-confirmation.html', context)

            email_instance = EmailMultiAlternatives('Account Activation Loyalty Rewards', text_content)
            email_instance.attach_alternative(html_content, "text/html")
            email_instance.to = [email]
            email_instance.send()
            data = {"success": True}
            return {"data": data, "message": "Please activate your account!!", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        print(e)
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}
