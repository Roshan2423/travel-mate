from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from pymongo import MongoClient
from django.conf import settings

User = get_user_model()

class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'],
                                 settings.DATABASES['default']['CLIENT']['port'],
                                 username=settings.DATABASES['default']['CLIENT']['username'],
                                 password=settings.DATABASES['default']['CLIENT']['password'],
                                 authSource=settings.DATABASES['default']['CLIENT']['authSource'])
            db = client[settings.DATABASES['default']['NAME']]
            collection = db['myapp_userlogindata']

            user_login_data = collection.find_one({'user_id': request.user.id})
            if not user_login_data:
                collection.insert_one({
                    'user_id': request.user.id,
                    'login_time': datetime.datetime.now(),
                    'ip_address': self.get_client_ip(request)
                })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
