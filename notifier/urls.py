from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('getall/', NotificationsViewSet.as_view(), name='user_notifications'),
    path('mark-as-read/<int:id>/', NotificationSetRead.as_view(), name='set_read'),
    path('mark-all-as-read/', AllNotificationSetRead.as_view(), name='set_all_read'),
]
