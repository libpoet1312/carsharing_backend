from django.http import JsonResponse, response
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *
from notifications.signals import notify


class RideListView(ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = TestRideSerializer
    permission_classes = [AllowAny, ]


class RideCreateView(CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideListSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = RideListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploader=request.user,
                            uploader_name=request.user.username
                            )
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideDetailView(RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = TestRideSerializer
    permission_classes = [AllowAny, ]


class RideEditView(RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = TestRideSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class getjoinRequests(RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = JoinRequestsSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class joinRequest(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)

        if ride.joinRequests.filter(pk=request.user.pk).exists() | ride.passengers.filter(pk=request.user.pk).exists():
            return JsonResponse('Already requested to join! Please wait for confirmation!', safe=False)

        ride.joinRequests.add(request.user)
        ride.save()

        notify.send(request.user, actor=request.user, recipient=ride.uploader, verb='Requested to Join', target=ride)

        return JsonResponse('Requested to Join', safe=False)


class canceljoinRequest(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)

        if not ride.joinRequests.filter(pk=request.user.pk).exists():
            return JsonResponse('Not Allowed!', safe=False)

        ride.joinRequests.remove(request.user)
        ride.save()

        # notify.send(request.user, recipient=ride.uploader, verb='Cancel request to Join', target=ride)

        return JsonResponse('Canceled Request to Join', safe=False)


class unJoin(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)

        if not ride.passengers.filter(pk=request.user.pk).exists():
            return JsonResponse('Not Allowed!', safe=False)

        ride.joinRequests.remove(request.user)
        ride.save()

        notify.send(request.user, recipient=ride.uploader, verb='Passenger cancelled!', target=ride)

        return JsonResponse('Passenger cancelled!', safe=False)


class kick(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk, userid):
        ride = get_object_or_404(Ride, pk=pk)
        self.check_object_permissions(request, ride)

        if not ride.passengers.filter(pk=userid).exists():
            return JsonResponse('doesnt exist!', safe=False)

        kickedUser = User.objects.get(pk=userid)

        ride.passengers.remove(kickedUser)
        ride.save()

        return JsonResponse('Kicked', safe=False)

class declineJoin(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk, userid):
        ride = get_object_or_404(Ride, pk=pk)
        self.check_object_permissions(request, ride)

        if not ride.joinRequests.filter(pk=userid).exists():
            return JsonResponse('doesnt exist!', safe=False)

        declinedUser = User.objects.get(pk=userid)

        ride.joinRequests.remove(declinedUser)
        ride.save()

        return JsonResponse('Declined Join', safe=False)


class acceptJoin(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk, userid):
        ride = Ride.objects.all().get(pk=pk)
        self.check_object_permissions(request, ride)

        if ride.joinRequests.count() == 0:
            return JsonResponse('Nothing to accept', safe=False)

        acceptedUser = User.objects.get(pk=userid)

        ride.joinRequests.remove(acceptedUser)

        ride.passengers.add(acceptedUser)
        ride.vacant_seats -= 1  # decrement vacant seats
        ride.save()

        notify.send(request.user, recipient=acceptedUser, target=ride, verb='Request to join' + str(ride) + 'Accepted')

        return JsonResponse('Accepted Join', safe=False)


class NotificationsViewSet(ListAPIView):
    serializer_class = NotificationsSerializer

    def list(self, request, **kwargs):
        queryset = request.user.notifications.all()
        return response(NotificationsSerializer(queryset).data)
