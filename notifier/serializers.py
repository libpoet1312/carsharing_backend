from rest_framework import serializers
from users.serializers import UserSerializer
from rides.serializers import RideListSerializer
from notifications.models import Notification


class NotificationsSerializer(serializers.ModelSerializer):
    actor = UserSerializer()
    recipient = UserSerializer()
    unread = serializers.BooleanField(read_only=True)
    target = RideListSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'recipient', 'verb', 'target', 'unread')
        depth = 0


class NotificationsEditSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    unread = serializers.BooleanField(read_only=True)
    target = RideListSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('slug', 'actor', 'recipient', 'verb', 'target', 'unread')
        depth = 1