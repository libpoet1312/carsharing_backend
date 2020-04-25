from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *
from notifications.signals import notify
from users.models import User
from .models import Ride, Request


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
            serializer.save(uploader=request.user)
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


class getRequests(RetrieveAPIView):

    serializer_class = RequestsSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        print(pk)
        ride = Ride.objects.get(pk=pk)
        qs = ride.request.all()
        return qs


class joinRequest(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)
        if ride.request.filter(pk=request.user.pk).exists() | Request.objects.all().filter(fromuser=request.user, ride=ride).exists():
            return JsonResponse('Already requested to join! Please wait for confirmation!', safe=False)

        print(request.data)

        no_seats = request.POST.get('seats')
        print(no_seats)

        # USER FHOTO URL!!!! HEHAHHAH
        #sprint(request.user.socialaccount_set.all()[0].get_avatar_url())

        Request.objects.create(
            fromuser=request.user,
            ride=ride,
            seats=no_seats,
        )

        notify.send(request.user, actor=request.user, recipient=ride.uploader, verb='Requested to Join', target=ride)

        return JsonResponse('Requested to Join', safe=False)


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

    def get(self, request, pk, userid):
        ride = get_object_or_404(Ride, pk=pk)
        self.check_object_permissions(request, ride)

        if not ride.request.filter(pk=userid).exists():
            return JsonResponse('doesnt exist!', safe=False)

        declinedUser = User.objects.get(pk=userid)

        req = Request.objects.all().get(fromuser=declinedUser, ride=ride)

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

        ride.vacant_seats -= 1  # decrement vacant seats
        ride.save()

        notify.send(request.user, recipient=acceptedUser, target=ride,
                    verb='Request to join ' + str(ride) + ' Accepted')

        return JsonResponse('Accepted Join', safe=False)
