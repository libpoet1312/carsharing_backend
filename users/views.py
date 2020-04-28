from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsUserOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User
from .serializers import UserSerializer, TestUserSerializer, CustomRegisterSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class UserView(ListAPIView):
    serializer_class = TestUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JSONWebTokenAuthentication,]


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = TestUserSerializer

    authentication_classes = [JSONWebTokenAuthentication,]
    pagination_class = None

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated,]
        if self.action == 'update' or self.action == 'partial_update':
            print('skata')
            self.permission_classes = [IsUserOrReadOnly]
        if self.action == 'create':
            self.permission_classes = [IsAdminUser,]

        return super(self.__class__, self).get_permissions()

