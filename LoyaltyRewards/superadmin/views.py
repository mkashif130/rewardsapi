from LoyaltyRewards.decorators import *
from LoyaltyRewards.utils import *
from store.models import Store


@authenticated_rest_call_super_admin(['GET'])
def get_request_logs(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        logs_ = LoggingOfEveryRequest.objects.all().order_by('-id')[:10]
        logs_list = []
        for obj in logs_:
            obj = json.loads(obj.log_data)
            log_data = {'remote_address': obj['remote_address'], 'server_hostname': obj['server_hostname'],
                        'request_method': obj['request_method'], 'request_path': obj['request_path'],
                        'run_time': obj['run_time'], 'request_body': obj['request_body'],
                        'response_body': obj['response_body'],
                        'is_authenticated': obj['is_authenticated']}
            logs_list.append(log_data)
        data = {"logs_list": logs_list}
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
        data = json.loads(request.body.decode('utf-8'))
        name = data['name'] if 'name' in data else None
        is_active = data['is_active'] if 'is_active' in data else True
        slogan = data['slogan'] if 'slogan' in data else ''
        description = data['description'] if 'description' in data else ''
        if name is None:
            data = {"success": False}
            return {"data": data, "message": "Name is required Field", "status": BAD_REQUEST_CODE}

        Store.objects.create(name=name, slogan=slogan, description=description,
                             added_by=request.user, is_active=is_active,
                             created_at=datetime.datetime.utcnow().timestamp(),
                             updated_at=datetime.datetime.utcnow().timestamp())
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
        data = json.loads(request.body.decode('utf-8'))
        name = data['name'] if 'name' in data else None
        is_active = data['is_active'] if 'is_active' in data else None
        slogan = data['slogan'] if 'slogan' in data else None
        description = data['description'] if 'description' in data else None
        store_id = data['store_id'] if 'store_id' in data else None
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
        stores = Store.objects.filter(is_removed=False)
        stores_list = []
        for obj in stores:
            stores_list.append(store_information(obj))
        data = {"stores_list": stores_list}
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
        logs_ = LogEntryForException.objects.all().order_by('-id')[:10]
        logs_list = []
        for obj in logs_:
            logs_list.append(obj.exception)
        data = {"logs_list": logs_list}
        return {"data": data, "message": "Log List", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}

