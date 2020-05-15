from rest_framework import serializers
from users.serializers import SimpleUserSerializer
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'


class SmallCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('plate',)
