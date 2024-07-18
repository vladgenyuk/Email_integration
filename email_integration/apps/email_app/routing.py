from django.urls import path
from .consumer import EmailConsumer

websocket_urlpatterns = [
    path('ws/email/', EmailConsumer.as_asgi()),
]
