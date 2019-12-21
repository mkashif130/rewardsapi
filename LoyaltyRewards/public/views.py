from LoyaltyRewards.decorators import *
from LoyaltyRewards.utils import *
from store.models import Store


@authenticated_rest_call(['GET'])
def dashboard(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        stores = Store.objects.filter(is_removed=False, is_active=True)
        stores_list = []
        for obj in stores:
            stores_list.append(store_information(obj))
        data = {"stores_list": stores_list}
        return {"data": data, "message": "Stores List", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}


