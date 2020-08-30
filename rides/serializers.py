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

    def update(self, instance, validated_data):
        print('update', flush=True)
        print(validated_data, flush=True)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.vacant_seats = validated_data.get('vacant_seats', instance.vacant_seats)
        # instance.car = validated_data.get('origin', instance.origin)
        car = validated_data.get('car')
        print(car['plate'], flush=True)
        instance.car = Car.objects.all().get(plate=car['plate'])
        instance.save()

        return instance


class CreatRideSerializer(serializers.ModelSerializer):
    uploader = SimpleUserSerializer(read_only=True)
    car = CarSerializer()

    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'uploader', 'car',)

        depth = 1

    def create(self, validated_data):
        return Ride.objects.create(**validated_data)
