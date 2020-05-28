from channels.routing import ProtocolTypeRouter, URLRouter  # changed
import rides.routing
from django_backend.json_token_auth import TokenAuthMiddlewareStack


# application = ProtocolTypeRouter({
#     'websocket': URLRouter([
#         path('ws/rides/', RideConsumer),
#     ]),
# })


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            rides.routing.websocket_urlpatterns
        )
    ),
})