import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from wagtail_live.publishers.django_channels import live_websocket_route

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wagtail_space_liveblog.settings.dev")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                live_websocket_route,
            )
        ),
    }
)
