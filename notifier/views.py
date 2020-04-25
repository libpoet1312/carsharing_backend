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
        print(self.queryset)
        print(kwargs['id'])
        notification = get_object_or_404(
            Notification, recipient=request.user, id=kwargs['id'])
        if not notification:
            return JsonResponse('Wrong', safe=False)

        notification.mark_as_read()
        return JsonResponse('okey', safe=False)


class AllNotificationSetRead(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationsViewSet
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        qs = self.queryset
        print(qs)
        qs.mark_all_as_read(request.user)

        return JsonResponse('okey', safe=False)