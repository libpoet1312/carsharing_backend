from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser


# def get_user_jwt(request):
#     user = get_user(request)
#
#     # if user.is_authenticated:
#     #     print('edw')
#     #     return user
#     try:
#         user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
#         #print('user_jwt', user_jwt)
#         if user_jwt is not None:
#             #print('asdasd')
#             return user_jwt[0]
#         else:
#             return AnonymousUser
#     except:
#         #print('skata')
#         user = AnonymousUser
#     #print('user=', user)
#
#     # if user.is_authenticated:
#     #     print('edw')
#     #     return user
#
#     return user
#
#
# class AuthenticationMiddlewareJWT(MiddlewareMixin):
#     def process_request(self, request):
#         assert hasattr(request,
#                        'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
#
#         request.user = SimpleLazyObject(lambda: get_user_jwt(request))
#         print('FROM MIDDLEWARE=', request.user)

class AuthenticationMiddlewareJWT(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        #print(request.user)
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):

        user = get_user(request)
        #print('FROM MIDDLEWARE=', user)
        if user.is_authenticated:
            return user
        try:
            user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
            if user_jwt is not None:
                return user_jwt[0]
        except:
            pass
        return user # AnonymousUser
