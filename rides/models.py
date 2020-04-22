from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
import datetime


class Ride(models.Model):
    TYPE = Choices(
        ('offer', 'Offer a ride'),
        ('request', 'Request a ride'),
    )

    origin = models.CharField(max_length=255, blank=False)
    destination = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=32, choices=TYPE, default=TYPE.offer)

    date = models.DateField(auto_now=True)
    time = models.TimeField(default=datetime.time(12, 00, 00))
    periodic = models.BooleanField(default=False)

    vacant_seats = models.IntegerField(verbose_name='Διαθέσιμες Θέσεις', blank=False)
    passengers = models.ManyToManyField(User, verbose_name='Επιβάτες', related_name='passengers', blank=True)

    joinRequests = models.ManyToManyField(User, verbose_name='Aιτήσεις', related_name='joinRequests', blank=True)

    uploader = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    uploader_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.origin + ' to ' + self.destination
