from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
#from .models import Notice, User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# 聊天用consumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #t = self.scope['user'].username
       # print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        #self.username = dict(self.scope['headers'])[b'user'].decode()
       # print(self.username)
        self.room_group_name = 'chat_%s' % self.room_name


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message,
        }))


# 推送consumer
class PushConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['username']
        print(self.channel_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            "event": event['event']
        }))


# 消息推送
def push(username, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username,
        {
            "type": "push.message",
            "event": event
        }
    )




