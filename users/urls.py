from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token
from .views import FacebookLogin, UserViewSet

urlpatterns = [
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('refresh-token/', refresh_jwt_token),

    path('users/', UserViewSet.as_view(), name='all_users')

    # path('accounts/', include('allauth.urls')),  # ?? ??
]
