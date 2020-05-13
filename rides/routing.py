from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'rides/<int:pk>', consumers.RideConsumer),
]