from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *


class RideListView(ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializerFull
    permission_classes = [AllowAny, ]


class RideCreateView(CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideListSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = RideListSerializer(data=request.data)
        if serializer.is_valid():
            print('FROM POST=', request.user)
            serializer.save(uploader=request.user,
                            uploader_name=request.user.username
                            )
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideDetailView(RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializerFull
    permission_classes = [AllowAny, ]


class RideEditView(RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializerFull
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


def JoinRequest(request, pk):
    ride = Ride.objects.all().get(pk=pk)
    print(ride)

    return JsonResponse('okey', safe=False)



def unJoin(request):
    pass


def declineJoin(request):
    pass


def acceptJoin(request):
    pass
