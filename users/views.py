from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User
from .serializers import UserSerializer, TestUserSerializer, CustomRegisterSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class UserViewSet(ListAPIView):
    serializer_class = TestUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JSONWebTokenAuthentication,]

