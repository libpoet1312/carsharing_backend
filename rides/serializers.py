from rest_framework import serializers
from rest_framework.serializers import StringRelatedField, RelatedField
from .models import Ride
from users.serializers import UserSerializer


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
    uploader = UserSerializer(read_only=True)

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



