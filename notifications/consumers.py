from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.checks import database
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async
import json

class NotificationHandler(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        id = self.scope.get('url_route').get('kwargs').get('user_id')
        self.group_name = f"notify_{id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def notify(self, event):
        user = await self.get_user(event.get('user_id'))
        html = await sync_to_async(render_to_string)('partial/notification_message.html#notification-return', {'user':user})
        await self.send(html)


    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)