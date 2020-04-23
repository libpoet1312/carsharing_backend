from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token
from .views import *
from rides.views import NotificationsViewSet

urlpatterns = [

    path('rest-auth/', include('rest_auth.urls')),

    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('refresh-token/', refresh_jwt_token),

    path('accounts/', include('allauth.urls')),

    path('not/getnot/', NotificationsViewSet.as_view(), name='user_notifications')
]
