import datetime
import qrcode
from registration.models import LogEntryForException, Profile
from .constants import *


def exception_log_entry(exception, requested_url=None, user_agent=None):
    LogEntryForException.objects.create(log_type=0, exception=exception, requested_url=requested_url,
                                        user_agent=user_agent)
    return True


def activate_user(user):
    user.is_active = True
    user.save()
    profile = Profile.objects.filter(user=user).last()
    profile.is_account_active = True
    profile.save()
    return 1


def login_signup_info(profile):
    name = ''
    image = DEFAULT_IMAGE
    if profile.name:  name = profile.name
    if profile.profile_image:  image = MEDIA_URL + str(profile.profile_image.url)
    name = profile.user.username
    try:
        name, id_ = name.split('@')
    except:
        pass

    profile_info = {
        "role": profile.role,
        "name": name,
        "logo_image": image}
    return profile_info


def retrieve_date_time(timestamp):
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    return {
        'date': datetime.datetime.strftime(timestamp, '%b %d, %Y'),
        'time': datetime.datetime.strftime(timestamp, '%I:%M %p')
    }


def store_information(store):
    if store.image:
        image = MEDIA_URL + str(store.image.url)
    else:
        image = ''

    if not store.qrcode:
        path_ = generate_qr_code(store.id)
        store.qrcode = path_
        store.save()

    qr_code_value = MEDIA_URL + '/' + store.qrcode

    return {
        'name': store.name,
        'description': store.description,
        'slogan': store.slogan,
        'is_active': store.is_active,
        'created_at': retrieve_date_time(store.created_at),
        'updated_at': retrieve_date_time(store.updated_at),
        'added_by': store.added_by.username,
        'store_id': store.id,
        'contact': store.contact,
        'latitude': store.latitude,
        'longitude': store.longitude,
        'address': store.address,
        'owner': store.owner,
        'image': image,
        'qrcode': qr_code_value
    }


def get_limit_and_page_from_request(request):
    data = request
    page = data['page'] if 'page' in data else DEFAULT_PAGE
    limit = data['limit'] if 'limit' in data else DEFAULT_LIMIT

    page = int(page)
    limit = int(limit)
    return page, limit


def generate_qr_code(store_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data({'store_id': int(store_id)})
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path_ = 'media/img' + str(store_id) + '.jpg'
    img.save('media/img' + str(store_id) + '.jpg')
    return path_
