"""
ASGI config for website project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import chats.routing, notifications.routing


application = ProtocolTypeRouter({
    'http':django_asgi_app,
    'websocket':AuthMiddlewareStack(
        URLRouter(chats.routing.websocket_urlpatterns + notifications.routing.websocket_urlpatterns)
    )
}
)
