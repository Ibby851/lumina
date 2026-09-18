from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import IndividualChat
import json

class IndividualChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.friend_id = self.scope.get('url_route').get('kwargs').get('friend_id')
        ids = sorted([self.user.id, self.friend_id])
        self.group_name = f"chat_{ids[0]}_{ids[1]}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data = None, bytes_data = None):
        data = json.loads(text_data)
        content = data.get('content')
        message = await self.save_message(self.user.id, self.friend_id, content)
        event = {
            'type':'broadcast_message',
            'message_id':message.id,
            'sender_id': self.user.id


        }
        await self.channel_layer.group_send(self.group_name, event)

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        return IndividualChat.objects.create(sender=sender, receiver=receiver, content=content)
    
    @database_sync_to_async
    def get_message(self, message_id):
        return IndividualChat.objects.get(id=message_id)

    async def broadcast_message(self, event):
        message_obj = await self.get_message(event.get('message_id'))
        html = render_to_string('partial/message-return.html#websocket-message', {'message': message_obj, 'is_sender': self.user.id == event.get('sender_id')})
        await self.send(html)




