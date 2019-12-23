import random

from LoyaltyRewards.decorators import *
from LoyaltyRewards.utils import *
from .models import *


@authenticated_rest_call(['GET'])
def dashboard(request):
    requested_url = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    try:
        stores = Store.objects.filter(is_removed=False, is_active=True)
        public = Public.objects.get(profile=request.profile)
        stores_list = []
        for obj in stores:
            store = store_information(obj)
            if PublicRedeems.objects.filter(store=obj, public=public).exists():
                store['points'] = PublicRedeems.objects.filter(store=obj, public=public).last().points
            else:
                store['points'] = 0
            store['points'] = random.randint(10, 1000)
            stores_list.append(store)
        total_points = public.total_points
        total_points = random.randint(15, 600)
        total_amount = random.randint(15, 600)
        name = public.profile.name
        data = {"stores_list": stores_list, 'name': name, 'total_points': total_points, 'total_amount': total_amount}
        return {"data": data, "message": "Stores List", "status": SUCCESS_RESPONSE_CODE}
    except Exception as e:
        exception_log_entry(e, requested_url, user_agent)
        data = {"success": False}
        return {"data": data, "message": "Something Went Wrong", "status": INTERNAL_SERVER_ERROR_CODE}
