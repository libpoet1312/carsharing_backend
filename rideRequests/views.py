from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from notifications.signals import notify
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json
from rides.permissions import IsOwnerOrReadOnly
from .models import Request
from rides.models import Ride
from .serializers import *
from rest_framework.generics import ListAPIView

User = get_user_model()


class getMyRequests(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = UserRequestsSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        req = Request.objects.all().filter(fromuser=self.request.user)
        # print(req)

        return req


class getAllRequests(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = CustomRequestsSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        rides = Ride.objects.all().filter(uploader=self.request.user)
        # print(rides)
        qs = []
        for ride in rides:
            qs += ride.request.all()
        return qs


class getRequestsforRide(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestsSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        # print(pk)
        ride = Ride.objects.get(pk=pk)
        self.check_object_permissions(self.request, ride)
        # print(ride)
        qs = ride.request.all()
        # print(qs)
        return qs


class joinRequest(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)
        if Request.objects.all().filter(fromuser=request.user, ride=ride).exists():
            return JsonResponse('Already requested to join! Please wait for confirmation!', safe=False)

        # print(json.loads(request.body.decode('utf-8')))
        body = json.loads(request.body.decode('utf-8'))

        no_seats = body['seats']
        # print(no_seats)
        if no_seats is None:
            return JsonResponse('Wrong format', safe=False, status=400)

        message = body['message']
        # print(message)

        # USER FHOTO URL!!!! HEHAHHAH
        # sprint(request.user.socialaccount_set.all()[0].get_avatar_url())

        req = Request.objects.create(
            fromuser=request.user,
            ride=ride,
            seats=no_seats,
            message=message,
            accepted=False
        )

        response = UserRequestsSerializer(instance=req).data
        # print(response)

        notify.send(request.user, actor=request.user, recipient=ride.uploader, verb='Requested to Join', target=ride)

        return JsonResponse(response, safe=False)


class unJoin(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)
        req = Request.objects.all().get(fromuser=request.user, ride=ride)
        if not req:
            return JsonResponse('WTF', safe=False)

        req.delete()

        # notify.send(request.user, recipient=ride.uploader, verb='Cancel request to Join', target=ride)

        return JsonResponse('Canceled Request to Join', safe=False)


class declineJoin(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk, userid):  # pk = ride pk, userid = user pk
        ride = get_object_or_404(Ride, pk=pk)
        self.check_object_permissions(request, ride)
        # print(ride.request.all())
        declinedUser = User.objects.get(pk=userid)
        req = Request.objects.all().get(fromuser=declinedUser, ride=ride)

        if not req:
            return JsonResponse('doesnt exist!', safe=False)

        req.delete()

        return JsonResponse('Declined Join', safe=False)


class acceptJoin(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk, userid):
        ride = Ride.objects.all().get(pk=pk)
        self.check_object_permissions(request, ride)

        if ride.request.count() == 0:
            return JsonResponse('Nothing to accept', safe=False)

        acceptedUser = User.objects.get(pk=userid)

        req = Request.objects.all().get(fromuser=acceptedUser, ride=ride)

        req.accepted = True
        req.save()

        ride.vacant_seats -= req.seats  # decrement vacant seats
        ride.save()

        notify.send(request.user, recipient=acceptedUser, target=ride,
                    verb='Request to join ' + str(ride) + ' Accepted')

        return JsonResponse('Accepted Join', safe=False)


@receiver(post_save, sender=Request)
def post_save_handler(sender, instance, created, **kwargs):
    # print(instance)
    print('ADD')
    ride = instance.ride
    channel_layer = get_channel_layer()
    # print(ride.uploader.pk)

    # send notification to uploader!
    JSONinstance = CustomRequestsSerializer(instance=instance).data
    if created:
        async_to_sync(channel_layer.group_send)(
            str(ride.uploader.pk),
            {
                "type": "addRequests",
                "text": JSONinstance
            }
        )
    else:
        async_to_sync(channel_layer.group_send)(
            str(instance.fromuser.pk),
            {
                "type": "updateRequests",
                "text": JSONinstance
            }
        )


# @receiver(pre_delete, sender=Request)
# def pre_delete_handler(sender, instance, **kwargs):
#     print('DELETE1')
#     ride = instance.ride
#     channel_layer = get_channel_layer()
#     # print(ride.uploader.pk)
#
#     # send notification to uploader!
#     JSONinstance = CustomRequestsSerializer(instance=instance).data
#
#     async_to_sync(channel_layer.group_send)(
#         str(ride.uploader.pk),
#         {
#             "type": "removeRequests",
#             "text": JSONinstance
#         }
#     )


@receiver(post_delete, sender=Request)
def pre_delete_handler(sender, instance, **kwargs):
    print('DELETE2')
    print(kwargs['signal'])
    ride = instance.ride
    channel_layer = get_channel_layer()
    # print(ride.uploader.pk)

    # send notification to uploader!
    JSONinstance = CustomRequestsSerializer(instance=instance).data

    async_to_sync(channel_layer.group_send)(
        str(instance.fromuser.pk),
        {
            "type": "removeMYRequests",
            "text": JSONinstance
        }
    )

    JSONinstance = CustomRequestsSerializer(instance=instance).data

    async_to_sync(channel_layer.group_send)(
        str(ride.uploader.pk),
        {
            "type": "removeRequests",
            "text": JSONinstance
        }
    )
