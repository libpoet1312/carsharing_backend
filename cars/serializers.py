from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'


class SmallCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('plate',)
