from LoyaltyRewards.decorators import *
from LoyaltyRewards.paginate import paginate
from LoyaltyRewards.utils import *
from store.models import Store, StoreOwner, StoreOffers
from public.models import PublicStore, Public

@authenticated_rest_call_super_admin(['GET'])
def get_request_logs(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        logs_ = LoggingOfEveryRequest.objects.all().order_by('-id')
        page, limit = get_limit_and_page_from_request(request.GET)

        def extract(obj):
            obj = json.loads(obj.log_data)
            log_data = {'remote_address': obj['remote_address'], 'server_hostname': obj['server_hostname'],
                        'request_method': obj['request_method'], 'request_path': obj['request_path'],
                        'run_time': obj['run_time'], 'request_body': obj['request_body'],
                        'response_body': obj['response_body'],
                        'is_authenticated': obj['is_authenticated']}
            return log_data

        data = paginate(logs_, extract, limit, page)
        return {"data": data, "message": "Log List", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['POST'])
def add_new_store(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = request.POST
        name = data['name'] if 'name' in data else None
        is_active = data['is_active'] if 'is_active' in data else True
        slogan = data['slogan'] if 'slogan' in data else ''
        description = data['description'] if 'description' in data else ''
        contact = data['contact'] if 'contact' in data else ''
        latitude = data['latitude'] if 'latitude' in data else 0
        longitude = data['longitude'] if 'longitude' in data else 0
        address = data['address'] if 'address' in data else ''
        owner = data['owner'] if 'owner' in data else ''
        owner_email = data['owner_email'] if 'owner_email' in data else None
        image = request.FILES['image'] if 'image' in request.FILES else None

        if owner_email is None:
            data = {"success": False}
            return {"data": data, "message": "Store Owner Email Is Required", "status": BAD_REQUEST_CODE}

        if name is None:
            data = {"success": False}
            return {"data": data, "message": "Name is required Field", "status": BAD_REQUEST_CODE}

        owner_email = owner_email.strip()
        owner_email = owner_email.lower()
        user_, created = User.objects.get_or_create(username=owner_email,
                                                    email=owner_email)
        user_.first_name = owner
        user_.save()
        profile, created = Profile.objects.get_or_create(user=user_)
        profile.name = owner
        profile.role = 3
        profile.save()

        store_owner, created = StoreOwner.objects.get_or_create(profile=profile)
        store_owner.name = owner
        store_owner.save()

        store_ = Store.objects.create(name=name, slogan=slogan, description=description,
                                      added_by=request.user, is_active=is_active,
                                      contact=contact, latitude=latitude, longitude=longitude,
                                      address=address, owner=owner,
                                      store_owner=store_owner,
                                      created_at=datetime.datetime.utcnow().timestamp(),
                                      updated_at=datetime.datetime.utcnow().timestamp())
        if image:
            store_.image = image
            store_.save()

        data = {"success": True}
        return {"data": data, "message": "Store successfully added", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['POST'])
def edit_store(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = request.POST
        name = data['name'] if 'name' in data else None
        is_active = data['is_active'] if 'is_active' in data else None
        slogan = data['slogan'] if 'slogan' in data else None
        description = data['description'] if 'description' in data else None
        store_id = data['store_id'] if 'store_id' in data else None
        contact = data['contact'] if 'contact' in data else ''
        latitude = data['latitude'] if 'latitude' in data else 0
        longitude = data['longitude'] if 'longitude' in data else 0
        address = data['address'] if 'address' in data else ''
        owner = data['owner'] if 'owner' in data else ''
        image = request.FILES['image'] if 'image' in request.FILES else None

        if store_id is None:
            data = {"success": False}
            return {"data": data, "message": "Store id is required for updation", "status": BAD_REQUEST_CODE}

        store = Store.objects.get(id=store_id)
        if name:
            store.name = name
        if is_active is not None:
            store.is_active = is_active
        if slogan:
            store.slogan = slogan
        if description:
            store.description = description
        if contact:
            store.contact = contact
        if latitude:
            store.latitude = latitude
        if longitude:
            store.longitude = longitude
        if address:
            store.address = address
        if owner:
            store.owner = owner
        if image:
            store.image = image

        store.updated_at = datetime.datetime.utcnow().timestamp()
        store.save()

        data = {"success": True}
        return {"data": data, "message": "Store successfully updated", "status": SUCCESS_RESPONSE_CODE}

    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['GET'])
def get_all_stores(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        page, limit = get_limit_and_page_from_request(request.GET)
        stores = Store.objects.filter(is_removed=False)

        def extract(obj):
            return store_information(obj)

        data = paginate(stores, extract, limit, page)
        return {"data": data, "message": "Stores List", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['DELETE'])
def delete_store(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = json.loads(request.body.decode('utf-8'))
        store_id = data['store_id'] if 'store_id' in data else None
        if store_id is None:
            data = {"success": False}
            return {"data": data, "message": "Store id is required for deletion", "status": BAD_REQUEST_CODE}
        store = Store.objects.get(id=store_id)
        store.is_removed = True
        store.save()
        data = {"success": True}
        return {"data": data, "message": "Deleted successfully", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['GET'])
def get_all_exceptions(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        page, limit = get_limit_and_page_from_request(request.GET)
        logs_ = LogEntryForException.objects.all().order_by('-id')

        def extract(obj):
            return obj.exception

        data = paginate(logs_, extract, limit, page)
        return {"data": data, "message": "Log List", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['POST'])
def add_new_offer(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = request.POST
        title = data['title'] if 'title' in data else None
        store_id = data['store_id'] if 'store_id' in data else None
        description = data['description'] if 'description' in data else ''
        image = request.FILES['image'] if 'image' in request.FILES else None
        is_valid = request.data['is_valid'] if 'is_valid' in data else None
        points = request.data['points'] if 'points' in data else 1

        points = int(points)

        if title is None:
            data = {"success": False}
            return {"data": data, "message": "Title is required Field", "status": BAD_REQUEST_CODE}

        if points is None:
            data = {"success": False}
            return {"data": data, "message": "points is required Field", "status": BAD_REQUEST_CODE}

        if store_id is None:
            data = {"success": False}
            return {"data": data, "message": "Store is required Field", "status": BAD_REQUEST_CODE}

        store = Store.objects.get(id=store_id)
        offer = StoreOffers.objects.create(store=store,
                                           title=title,
                                           points=points,
                                           description=description,
                                           created_at=datetime.datetime.utcnow().timestamp(),
                                           updated_at=datetime.datetime.utcnow().timestamp()
                                           )
        if image:
            offer.banner = image

        if is_valid is not None:
            if is_valid == 'true':
                is_valid = True
            else:
                is_valid = False
            offer.is_valid = is_valid
        offer.save()

        data = {"success": True}
        return {"data": data, "message": "Store offer successfully added", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['POST'])
def edit_store_offer(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = request.POST
        title = data['title'] if 'title' in data else None
        store_id = data['store_id'] if 'store_id' in data else None
        offer_id = data['offer_id'] if 'offer_id' in data else None
        is_valid = data['is_valid'] if 'is_valid' in data else None
        description = data['description'] if 'description' in data else ''
        points = data['points'] if 'points' in data else 1
        image = request.FILES['image'] if 'image' in request.FILES else None

        points = int(points)

        if offer_id is None:
            data = {"success": False}
            return {"data": data, "message": "Offer ID is required Field", "status": BAD_REQUEST_CODE}

        offer = StoreOffers.objects.get(id=int(offer_id))
        if store_id:
            store = Store.objects.get(id=store_id)
            offer.store = store

        if title:
            offer.title = title

        if description:
            offer.description = description

        if image:
            offer.banner = image

        offer.points = points

        if is_valid is not None:
            if is_valid == 'true':
                is_valid = True
            else:
                is_valid = False
            offer.is_valid = is_valid

        offer.updated_at = datetime.datetime.utcnow().timestamp()
        offer.save()

        data = {"success": True}
        return {"data": data, "message": "Store offer successfully added", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['DELETE'])
def delete_store_offer(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        data = json.loads(request.body.decode('utf-8'))
        offer_id = data['offer_id'] if 'offer_id' in data else None
        if offer_id is None:
            data = {"success": False}
            return {"data": data, "message": "Offer id is required for deletion", "status": BAD_REQUEST_CODE}
        offer_id = StoreOffers.objects.get(id=offer_id)
        offer_id.is_removed = True
        offer_id.save()
        data = {"success": True}
        return {"data": data, "message": "Deleted successfully", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


@authenticated_rest_call_super_admin(['POST'])
def create_random_my_stores(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        import random
        public = Public.objects.all()
        for obj in public:
            store = Store.objects.all().order_by('?')[0]
            PublicStore.objects.create(store=store,
                                       public=obj,
                                       points=random.randint(1,80),
                                       created_at=datetime.datetime.now().timestamp())
        data = {"success": True}
        return {"data": data, "message": "Deleted successfully", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}