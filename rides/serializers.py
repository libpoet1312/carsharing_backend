from rest_framework import serializers
from rest_framework.serializers import StringRelatedField, RelatedField
from .models import Ride, Request
from users.serializers import UserSerializer, TestUserSerializer


class RequestsSerializer(serializers.ModelSerializer):
    fromuser = TestUserSerializer()

    class Meta:
        model = Request
        fields = ('fromuser', 'seats', 'accepted',)
        depth = 2


class TestRideSerializer(serializers.ModelSerializer):
    uploader = TestUserSerializer(read_only=True)
    request = RequestsSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'car', 'uploader', 'request')

        depth = 2


class RideListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  )


class CostumRequestsSerializer(serializers.ModelSerializer):
    fromuser = TestUserSerializer()
    ride = RideListSerializer()

    class Meta:
        model = Request
        fields = ('fromuser', 'seats', 'accepted', 'ride')
        depth = 2


