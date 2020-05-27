import datetime
import json
from json import loads

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.core.serializers import serialize
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from notifier.serializers import NotificationsSerializer
from notifications.models import Notification
from rides.permissions import IsOwnerOrReadOnly


# GET ALL NOTIFICATIONSs
class NotificationsViewSet(ListAPIView):
    serializer_class = NotificationsSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        print('user = ', self.request.user)
        queryset = self.request.user.notifications.all()
        return queryset


# Set Notification as READ
class NotificationSetRead(RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationsViewSet
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        # print(self.queryset)
        # print(kwargs['id'])
        notification = get_object_or_404(
            Notification, recipient=request.user, id=kwargs['id'])
        if not notification:
            return JsonResponse('Wrong', safe=False)

        notification.mark_as_read()
        return JsonResponse('okey', safe=False)


class AllNotificationSetRead(ListAPIView):
    queryset = Notification.objects.all()
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        qs = self.queryset
        # print(qs)
        user = request.user

        user.notifications.mark_all_as_read()

        JSONqs = NotificationsSerializer(user.notifications, many=True).data

        return JsonResponse(JSONqs, safe=False)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

    if isinstance(o, datetime.date):
        return o.__str__()

    if isinstance(o, datetime.time):
        return o.__str__()


@receiver(post_save, sender=Notification)
def post_save_handler(sender, instance, created, **kwargs):

    if created:
        channel_layer = get_channel_layer()
        # print(instance.target.uploader)

        # serialized_obj = serializers.serialize('json', [ instance, ])
        serialized_obj = NotificationsSerializer(instance).data
        s = json.dumps(serialized_obj, default=myconverter)
        # print(s)

        # send notif to ride uploader
        if instance.verb == 'request' or instance.verb == 'cancelRequest':
            print(instance.target.uploader)
            async_to_sync(channel_layer.group_send)(
                str(instance.target.uploader.pk),
                {
                    "type": "sendNotification",
                    "text": s
                }
            )
        # send notif to user that requested
        elif instance.verb == 'accepted' or instance.verb == 'declineRequest':
            print(instance.recipient)
            async_to_sync(channel_layer.group_send)(
                str(instance.recipient.pk),
                {
                    "type": "sendNotification",
                    "text": s
                }
            )