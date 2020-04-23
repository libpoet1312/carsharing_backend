from rest_framework import serializers
from rest_framework.serializers import StringRelatedField, RelatedField
from .models import Ride
from django.contrib.auth.models import User
from notifications.models import Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username',)


class TestRideSerializer(serializers.ModelSerializer):
    joinRequests = UserSerializer(many=True)
    uploader = UserSerializer()
    passengers = UserSerializer(many=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'passengers', 'joinRequests', 'uploader')

        depth = 1


class RideListSerializer(serializers.ModelSerializer):
    uploader = UserSerializer()

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'uploader',)


class JoinRequestsSerializer(serializers.ModelSerializer):
    # joinRequests = StringRelatedField(read_only=True, many=True)
    joinRequests = UserSerializer(many=True)

    class Meta:
        model = Ride
        fields = ('joinRequests',)
        depth = 1


class NotificationsSerializer(serializers.ModelSerializer):
    actor = UserSerializer
    recipient = UserSerializer
    unread = serializers.BooleanField(read_only=True)
    target = RideListSerializer

    class Meta:
        model = Notification
        fields = ('actor', 'recipient', 'verb', 'target', 'unread')
        depth = 0
