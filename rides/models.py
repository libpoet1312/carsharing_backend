from django.db import models
from django_backend import settings
from model_utils import Choices
from cars.models import Car
import datetime


class Ride(models.Model):
    TYPE = Choices(
        ('offer', 'Offer a ride'),
        ('request', 'Request a ride'),
    )

    origin = models.CharField(max_length=255, blank=False)
    destination = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=32, choices=TYPE, default=TYPE.offer)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car', null=True)

    date = models.DateField(auto_now=True)
    time = models.TimeField(default=datetime.time(12, 00, 00))
    periodic = models.BooleanField(default=False)

    vacant_seats = models.IntegerField(verbose_name='Διαθέσιμες Θέσεις', blank=False)

    #  Ride properties  #
    smoking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    music = models.BooleanField(default=True)
    chat = models.BooleanField(default=True)

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='uploader')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.origin + ' to ' + self.destination


class Request(models.Model):
    fromuser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request')
    ride = models.ForeignKey(Ride, related_name='request', on_delete=models.CASCADE)
    seats = models.IntegerField(default=1)

    accepted = models.BooleanField(default=False)

    def __str__(self):
        return '%d seat from %s for %s' % (self.seats, self.fromuser, self.ride)