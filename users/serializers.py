from rest_framework import serializers
from allauth.account.adapter import get_adapter

from rideRequests.serializers import UserRequestsSerializer
from .models import User
from rest_auth.registration.serializers import RegisterSerializer


class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('pk', 'email', 'username', 'phone_number', 'avatar', 'gender', 'dob', 'country', 'date_joined',
                  'has_whatsup', 'has_viber',)
        depth = 1


class MyUserSerializer(serializers.ModelSerializer):
    request = UserRequestsSerializer(many=True)
    notifications = serializers.SerializerMethodField()
    requestsOfMyRides = serializers.SerializerMethodField()
    car = serializers.SerializerMethodField(method_name="get_car")
    avatar = serializers.ImageField(default='avatar/default-avatar.jpg')

    class Meta:
        model = User
        fields = ('pk', 'email', 'username', 'phone_number', 'avatar', 'gender', 'dob', 'country', 'date_joined',
                  'has_whatsup', 'has_viber', 'car', 'request', 'requestsOfMyRides', 'notifications',)
        depth = 2

    def requestsOfMyRides(self):
        from rideRequests.serializers import RequestsSerializer
        print('requestsOfMyRides')
        return RequestsSerializer(many=True).data

    def get_notifications(self, obj):
        print('edw')
        from notifier.serializers import NotificationsSerializer
        print(obj)
        return NotificationsSerializer(obj.notifications.all(), many=True).data

    def get_car(self, obj):
        print("car")
        from cars.serializers import CarSerializer
        return CarSerializer(obj.car.all(), many=True).data

    # def update(self, instance, validated_data):
    #     print('MyUserSerializer', flush=True)
    #     print(validated_data, flush=True)
    #     if(validated_data['avatar']):
    #         instance.avatar = validated_data['avatar']
    #     instance.save()
    #     return instance


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'avatar')


class CustomRegisterSerializer(RegisterSerializer):
    country = serializers.CharField(required=False)
    has_whatsup = serializers.BooleanField(required=False, default=False)
    has_viber = serializers.BooleanField(required=False, default=False)
    is_confirmed = serializers.BooleanField(default=True, required=False, read_only=True)
    avatar = serializers.ImageField(default='avatar/default-avatar.jpg')

    dob = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'phone_number', 'avatar', 'gender', 'dob', 'country', 'has_whatsup',
            'has_viber', 'is_confirmed')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'avatar': self.validated_data.get('avatar', ''),
            'gender': self.validated_data.get('gender', ''),
            'country': self.validated_data.get('country', ''),
            'has_whatsup': self.validated_data.get('has_whatsup', ''),
            'has_viber': self.validated_data.get('has_viber', ''),
            'dob': self.validated_data.get('dob', ''),
        }

    def save(self, request):
        print(request.data, flush=True)
        adapter = get_adapter()
        # adapter = UserAdapter
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()
        # user = adapter.save_user(request, user, self, commit=False)

        print(user)

        user.phone_number = self.cleaned_data.get('phone_number')
        user.avatar = self.cleaned_data.get('avatar')

        user.gender = self.cleaned_data.get('gender')
        user.country = self.cleaned_data.get('country')
        user.has_whatsup = self.cleaned_data.get('has_whatsup')
        user.has_viber = self.cleaned_data.get('has_viber')
        user.dob = self.cleaned_data.get('dob')

        print('username', self.cleaned_data.get('username'))
        print('password1', self.cleaned_data.get('password1'))
        print('password2', self.cleaned_data.get('password2'))
        print('email', self.cleaned_data.get('email'))
        print('phone_number', self.cleaned_data.get('phone_number'))
        print('avatar', self.cleaned_data.get('avatar'))
        print('gender', self.cleaned_data.get('gender'))
        print('dob', self.cleaned_data.get('dob'))

        print(self.cleaned_data.get('country'))
        print(self.cleaned_data.get('has_whatsup'))
        print(self.cleaned_data.get('has_viber'))

        adapter.save_user(request, user, self)
        user.save()
        return user
