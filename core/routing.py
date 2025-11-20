from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from delivery.consumers import DeliveryLocationConsumer
from users.middleware import JwtAuthMiddleware

# WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/delivery/location/', DeliveryLocationConsumer.as_asgi()),
    # You can add more routes like:
    # path('ws/order/<int:order_id>/', DeliveryLocationConsumer.as_asgi()),
]

# ProtocolTypeRouter with custom JWT middleware wrapping the WebSocket routes.
application = ProtocolTypeRouter({
    "websocket": JwtAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
