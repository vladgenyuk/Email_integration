import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_integration.settings.dev')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.email_app.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
