from rest_framework import serializers
from .models import User
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField


class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('pk', 'email', 'username', 'phone_number', 'avatar', 'gender', 'dob', 'country', 'date_joined',
                   'has_whatsup', 'has_viber', )
        depth = 2


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username',)


class CustomRegisterSerializer(RegisterSerializer):
    phone_number = PhoneNumberField(required=False)
    avatar = serializers.ImageField(required=False)
    gender = serializers.ChoiceField(choices=User.GENDER)
    country = serializers.CharField(required=False)
    has_whatsup = serializers.BooleanField(required=False, default=False)
    has_viber = serializers.BooleanField(required=False, default=False)
    is_confirmed = serializers.BooleanField(default=True, required=False, read_only=True)


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
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.phone_number = self.cleaned_data.get('phone_number')
        user.avatar = self.cleaned_data.get('avatar')
        user.gender = self.cleaned_data.get('gender')
        user.country = self.cleaned_data.get('country')
        user.has_whatsup = self.cleaned_data.get('has_whatsup')
        user.has_viber = self.cleaned_data.get('has_viber')

        print('username', self.cleaned_data.get('username'))
        print('password1',self.cleaned_data.get('password1'))
        print('password2',self.cleaned_data.get('password2'))
        print('email',self.cleaned_data.get('email'))
        print('phone_number',self.cleaned_data.get('phone_number'))
        print('avatar',self.cleaned_data.get('avatar'))
        print(self.cleaned_data.get('gender'))
        print(self.cleaned_data.get('country'))
        print(self.cleaned_data.get('has_whatsup'))
        print(self.cleaned_data.get('has_viber'))

        user.save()
        adapter.save_user(request, user, self)
        return user
