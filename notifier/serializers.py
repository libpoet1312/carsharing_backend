from rest_framework import serializers
from users.serializers import SimpleUserSerializer
from rides.serializers import RideListSerializer
from notifications.models import Notification


class NotificationsSerializer(serializers.ModelSerializer):
    actor = SimpleUserSerializer()
    recipient = SimpleUserSerializer()
    unread = serializers.BooleanField(read_only=True)
    target = RideListSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'recipient', 'verb', 'target', 'unread', 'timestamp')
        depth = 1


class NotificationsEditSerializer(serializers.ModelSerializer):
    actor = SimpleUserSerializer(read_only=True)
    recipient = SimpleUserSerializer(read_only=True)
    unread = serializers.BooleanField(read_only=True)
    target = RideListSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('slug', 'actor', 'recipient', 'verb', 'target', 'unread')
        depth = 1