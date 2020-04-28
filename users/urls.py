from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework import routers
from .views import *

urlpatterns = [
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('refresh-token/', refresh_jwt_token),

    path('users/', UserView.as_view(), name='all_users'),

    #path('users/<int:pk>', UserUpdate.as_view(), name='update_user'),


    # path('accounts/', include('allauth.urls')),  # ?? ??
]


router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
urlpatterns += router.urls