from rest_framework import serializers
from .models import Request


class UserRequestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = ('seats', 'accepted', 'message', 'ride')
        depth = 3


class RequestsSerializer(serializers.ModelSerializer):
    from users.serializers import SimpleUserSerializer
    fromuser = SimpleUserSerializer()


    class Meta:
        model = Request
        fields = ('fromuser', 'seats', 'accepted', 'message')
        depth = 2



class CostumRequestsSerializer(serializers.ModelSerializer):
    #fromuser = TestUserSerializer()
    # ride = RideListSerializer()

    class Meta:
        model = Request
        fields = ('fromuser', 'seats', 'accepted', 'ride')
        depth = 2