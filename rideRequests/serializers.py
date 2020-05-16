from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Request
User = get_user_model()

class UserRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('pk', 'seats', 'accepted', 'message', 'ride',)
        depth = 1


class RequestsSerializer(serializers.ModelSerializer):
    fromuser = UserRequestsSerializer()

    class Meta:
        model = Request
        fields = ('pk', 'fromuser', 'seats', 'accepted', 'message')
        depth = 2


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'avatar')


class CustomRequestsSerializer(serializers.ModelSerializer):
    fromuser = SimpleUserSerializer()
    # ride = RideListSerializer()

    class Meta:
        model = Request
        fields = ('pk', 'fromuser', 'seats', 'accepted', 'ride')
        depth = 1
