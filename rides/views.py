from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import RideListSerializer, TestRideSerializer, OwnerSingleRideSerializer, \
    AuthenticatedSingleRideSerializer, AnonymousSingleRideSerializer
from notifications.signals import notify
from users.models import User
from .models import Ride


class RideListView(ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideListSerializer
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
    authentication_classes = [JSONWebTokenAuthentication]

    def get_serializer_class(self):
        #print(self.request.user)
        if self.request.user.is_authenticated:
            if self.get_object().uploader == self.request.user:
                serializer_class = OwnerSingleRideSerializer
            else:
                serializer_class = AuthenticatedSingleRideSerializer
        else:
            #print('edw')
            serializer_class = AnonymousSingleRideSerializer
        return serializer_class


class RideEditView(RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = TestRideSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



