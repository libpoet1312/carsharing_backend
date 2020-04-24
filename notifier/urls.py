from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('getall/', NotificationsViewSet.as_view(), name='user_notifications'),
    path('mark-read/<int:id>/', NotificationSetRead.as_view(), name='set_read'),
    path('setread/<int:pk>/', NotificationSetRead.as_view(), name='set_read'),
]
