from rest_framework import serializers
from rest_framework.serializers import StringRelatedField, RelatedField
from .models import Ride

from users.serializers import SimpleUserSerializer, TestUserSerializer
from rideRequests.serializers import RequestsSerializer
from cars.serializers import CarSerializer
from cars.models import Car


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
    time = serializers.TimeField(required=False)

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
    car = CarSerializer()

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'uploader', 'request', 'car',)

        depth = 1

    def create(self, validated_data):
        print('create', flush=True)
        return Ride.objects.create(**validated_data)


class CreatRideSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)
    car = CarSerializer()

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'uploader','car',)

        depth = 1

    def create(self, validated_data):
        return Ride.objects.create(**validated_data)