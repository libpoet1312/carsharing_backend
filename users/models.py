from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from model_utils import Choices
import datetime


class User(AbstractUser):
    GENDER = Choices(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    dob = models.DateField(max_length=8, default=datetime.date(1999, 12, 31))
    phone_number = models.TextField(max_length=12, blank=True, null=True, verbose_name='Τηλέφωνο')  # Τηλέφωνο
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default-avatar.jpg', blank=True)
    gender = models.CharField(blank=True, null=True, max_length=1, default=GENDER.O, choices=GENDER, verbose_name='Φύλο')
    country = models.CharField(max_length=3, blank=True, verbose_name='Χώρα', null=True)

    has_whatsup = models.BooleanField(blank=True, null=True, verbose_name='Whats up messenger platform')
    has_viber = models.BooleanField(blank=True, null=True, verbose_name='Viber messenger platform')

    is_confirmed = models.BooleanField(default=True, verbose_name='Επιβεβαιωμένος χρήστης')
    # for future confirmation by admins of user ID or PASSPORT

    class Meta:
        verbose_name_plural = 'Χρήστες'
        verbose_name = 'Χρήστης'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return "user/%s" % self.username



