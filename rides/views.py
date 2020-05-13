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

    def get_queryset(self):
        queryset = Ride.objects.all()
        origin = self.request.query_params.get('origin', None)
        #print(origin)
        if origin is not None:
            queryset = queryset.filter(origin__contains=origin)

        destination = self.request.query_params.get('destination', None)
        if destination is not None:
            queryset = queryset.filter(destination__contains=destination)

        date = self.request.query_params.get('date', None)
        if date is not None:
            print(date)
            queryset = queryset.filter(date=date)

        vacant_seats = self.request.query_params.get('passengers', None)
        if vacant_seats is not None:
            print(vacant_seats)
            queryset = queryset.filter(vacant_seats__gte=vacant_seats)

        return queryset


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


class getAllRequests(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = CostumRequestsSerializer
    #authentication_classes = JSONWebTokenAuthentication
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        rides = Ride.objects.all().filter(uploader=self.request.user)
        print(rides)
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
        print(pk)
        ride = Ride.objects.get(pk=pk)
        self.check_object_permissions(self.request, ride)
        print(ride)
        qs = ride.request.all()
        print(qs)
        return qs


class joinRequest(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        ride = Ride.objects.all().get(pk=pk)
        if Request.objects.all().filter(fromuser=request.user, ride=ride).exists():
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

    def get(self, request, pk, userid):  # pk = ride pk, userid = user pk
        ride = get_object_or_404(Ride, pk=pk)
        self.check_object_permissions(request, ride)
        print(ride.request.all())
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
