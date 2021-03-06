from urllib.request import urlopen

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.core.files.base import ContentFile
from django.dispatch import receiver
from rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsUserOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User
from .serializers import TestUserSerializer, CustomRegisterSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class UserView(ListAPIView):
    serializer_class = TestUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JSONWebTokenAuthentication]


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = TestUserSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JSONWebTokenAuthentication, ]
    pagination_class = None

    def get_permissions(self):
        print('From VIEW: ')
        print(self.request.user)

        if self.action == 'list':
            print('edw')
            self.permission_classes = [IsAuthenticated, ]
        if self.action == 'update' or self.action == 'partial_update':
            print('skata')
            self.permission_classes = [IsUserOrReadOnly, ]
        if self.action == 'create':
            self.permission_classes = [IsAdminUser, ]

        return super(self.__class__, self).get_permissions()


@receiver(user_signed_up)
def populate_profile(request, user, **kwargs):
    print('populate_profile', flush=True)
    print(user, flush=True)
    try:

        user_data = SocialAccount.objects.filter(user=user, provider='facebook')[0].extra_data
        obj = SocialAccount.objects.filter(user=user, provider='facebook')[0]

        print(obj, flush=True)
        print(user_data, flush=True)
        picture_url = "http://graph.facebook.com/" + user_data['id'] + "/picture?type=large"

        ph = urlopen(picture_url)
        print(ph, flush=True)

        user.avatar.save((user.username + " social") + '.jpg', ContentFile(ph.read()))

        user.fullname = user_data['name']
        user.save()
    except:
        return
        # if sociallogin.account.provider == 'facebook':
        #     user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        #     picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
        #     print(user.socialaccount_set.filter(provider='facebook'), flush=True)
        #     print(user.socialaccount_set.filter(provider='facebook')[0], flush=True)
        #     print(user_data, flush=True)
        #     first_name = user_data['first_name']
        #     ph = urlopen(picture_url)
        #     print(ph, flush=True)

        #     user.avatar.save((user.username + " social") + '.jpg',
        #                     ContentFile(ph.read()))

        #     user.fullname = user_data['name']
        #     user.save()
