from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field


class UserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        dob = data.get('dob')
        phone_number = data.get('phone_number')
        gender = data.get('gender')
        print('DOBBBB')
        print(dob)
        if dob:
            setattr(user, 'dob', dob)
        if phone_number:
            user_field(user, 'phone_number', phone_number)
        if gender:
            user_field(user, 'gender', gender)
        return super().save_user(request, user, form, commit=commit)
