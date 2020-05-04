from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .permissions import IsCarOwnerOrReadOnly
from .models import Car
from .serializers import CarSerializer
from rest_framework import viewsets


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    pagination_class = None
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        #print(queryset)
        queryset = Car.objects.all().filter(owner=self.request.user)
        print(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':

            print(self.request.data)
            self.permission_classes = [IsCarOwnerOrReadOnly,]

        return super(self.__class__, self).get_permissions()




