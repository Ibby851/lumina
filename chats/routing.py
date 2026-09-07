
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat-with/<int:friend_id>/', consumers.IndividualChatConsumer.as_asgi(), name='chat_friend'),
]