from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import RideListSerializer, TestRideSerializer, OwnerSingleRideSerializer, \
    AuthenticatedSingleRideSerializer, AnonymousSingleRideSerializer, CreatRideSerializer
from .models import Ride
from rest_framework import viewsets
from cars.models import Car


class MyRidesListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = OwnerSingleRideSerializer

    def get_queryset(self):
        queryset = Ride.objects.all().filter(uploader=self.request.user).order_by('created')
        # print(queryset)

        return queryset


class RideListView(ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideListSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        queryset = Ride.objects.all().order_by('created')
        origin = self.request.query_params.get('origin', None)
        # print(origin)
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
    serializer_class = CreatRideSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = CreatRideSerializer(data=request.data)
        # print(request.data['car'], flush=True)
        # print(serializer.is_valid(), flush=True)
        if serializer.is_valid(raise_exception=True):

            ride = serializer.save(uploader=request.user, car=Car.objects.all().get(pk=request.data['car']['id']))

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', flush=True)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideDetailView(RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = TestRideSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_serializer_class(self):
        # print(self.request.user)
        if self.request.user.is_authenticated:
            if self.get_object().uploader == self.request.user:
                # print('owner', flush=True)
                serializer_class = OwnerSingleRideSerializer
            else:
                # print('authenticated', flush=True)
                serializer_class = AuthenticatedSingleRideSerializer
        else:
            # print('edw')
            serializer_class = AnonymousSingleRideSerializer
        return serializer_class


class RideEditView(RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = OwnerSingleRideSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



