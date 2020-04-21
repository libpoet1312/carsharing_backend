from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices


class Ride(models):
    TYPE = Choices(
        ('offer', 'offer a ride'),
        ('request', 'request a ride'),
    )

    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    ride = models.CharField(max_length=32, choices=TYPE, default=TYPE.offer)
    time = models.DateTimeField()
    vacant_seats = models.IntegerField(default=1)
    passengers = models.ManyToManyField(User)

    uploader = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
