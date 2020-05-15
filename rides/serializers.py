from rest_framework import serializers
from rest_framework.serializers import StringRelatedField, RelatedField
from .models import Ride

from users.serializers import SimpleUserSerializer, TestUserSerializer
from rideRequests.serializers import RequestsSerializer


class TestRideSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)
    request = RequestsSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'car', 'uploader', 'request')

        depth = 1


class RideListSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats', 'uploader',
                  )

        depth = 1


class AnonymousSingleRideSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats', 'uploader',
                  )
        depth = 1


class AuthenticatedSingleRideSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'car', 'uploader',)

        depth = 1


class OwnerSingleRideSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)
    request = RequestsSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'car', 'uploader', 'request')

        depth = 1



