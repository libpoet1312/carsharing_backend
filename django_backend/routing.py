from channels.routing import ProtocolTypeRouter, URLRouter # changed
from django.urls import path # new
from rides.consumers import RideConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/rides/', RideConsumer),
    ]),
})