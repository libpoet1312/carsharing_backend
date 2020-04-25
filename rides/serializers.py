from rest_framework import serializers
from rest_framework.serializers import StringRelatedField, RelatedField
from .models import Ride, Request
from users.serializers import UserSerializer, TestUserSerializer

class RequestsSerializer0(serializers.ModelSerializer):
    fromuser = TestUserSerializer()


    class Meta:
        model = Request
        fields = ('fromuser', 'seats', 'accepted',)
        depth = 2


class TestRideSerializer(serializers.ModelSerializer):
    uploader = TestUserSerializer()
    request = RequestsSerializer0

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'car', 'request', 'uploader')

        depth = 2


class RideListSerializer(serializers.ModelSerializer):
    uploader = TestUserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'uploader',)


class RequestsSerializer(serializers.ModelSerializer):
    fromuser = UserSerializer
    ride = RideListSerializer()

    class Meta:
        model = Request
        fields = ('fromuser', 'ride', 'seats', 'accepted',)
        depth = 2



