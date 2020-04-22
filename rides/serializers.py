from rest_framework import serializers
from .models import Ride


class RideSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'passengers', 'joinRequests', 'uploader_name')


class RideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('pk', 'origin', 'destination', 'type',
                  'date', 'time', 'periodic', 'vacant_seats',
                  'uploader_name')