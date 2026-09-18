from django.urls import path
from . import consumers
websocket_urlpatterns = [
    path('ws/notify/<int:user_id>/', consumers.NotificationHandler.as_asgi()),
]