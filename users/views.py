from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer,TestUserSerializer
from rest_framework.generics import ListAPIView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class UserViewSet(ListAPIView):
    serializer_class = TestUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None

