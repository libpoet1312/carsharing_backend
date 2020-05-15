from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_backend import settings
from rides.models import Ride


class Request(models.Model):
    fromuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request')
    ride = models.ForeignKey(Ride, related_name='request', on_delete=models.CASCADE)
    seats = models.IntegerField(default=1)
    message = models.TextField(max_length=200, null=True, blank=True)

    accepted = models.BooleanField(default=False)

    def __str__(self):
        return '%d seat from %s for %s' % (self.seats, self.fromuser, self.ride)


@receiver(post_save, sender=Request)
def post_save_handler(sender, instance, created, **kwargs):
    print(instance)
    issuer = instance.fromuser
    channel_layer = get_channel_layer()
    print(issuer)

    async_to_sync(channel_layer.group_send)(
        issuer.username,
        {
            "type": "book.gossip",
            "message": instance
        }
    )