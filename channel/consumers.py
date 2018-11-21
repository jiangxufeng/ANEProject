from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async
from account.models import LoginUser
from rest_framework.authtoken.models import Token
import hashlib
from rewrite.exception import FoundUserFailed, MissingParameter, MyAuthenticationFailed


# 自定义websocket处理类
class ChatConsumer(AsyncJsonWebsocketConsumer):
    chats = dict()

    async def connect(self):
        headers = dict(self.scope['headers'])
        sign = headers.get(b'sign').decode() if headers.get(b'sign') else None
        timestamp = headers.get(b'timestamp').decode() if headers.get(b'timestamp') else None
        pk = headers.get(b'nameplate').decode() if headers.get(b'nameplate') else None
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        if not sign:
            self.close()

        if not pk:
            self.close()

        if not timestamp:
            self.close()

        try:
            user = await self.get_user(pk=pk[3:-2])
            token = await self.get_token(user)
            res = str(str(user.id) + token + timestamp)
        except LoginUser.DoesNotExist:
            self.close()

        else:
            if hashlib.md5(res.encode()).hexdigest() == sign:

                await self.channel_layer.group_add(self.group_name, self.channel_name)
                # 将用户添加至聊天组信息chats中
                try:
                    ChatConsumer.chats[self.group_name].add(self)
                except:
                    ChatConsumer.chats[self.group_name] = set([self])

                await self.accept()
            else:
                self.close()

    async def receive_json(self, message, **kwargs):
        # 收到信息时调用
        to_user = message.get('to_user')
        # 信息发送
        length = len(ChatConsumer.chats[self.group_name])
        if length == 2:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message.get('message'),
                },
            )
        else:
            await self.channel_layer.group_send(
                to_user,
                {
                    "type": "push.message",
                    "event": {'message': message.get('message'), 'group': self.group_name}
                },
            )

    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # 将该用户移除聊天组连接信息
        ChatConsumer.chats[self.group_name].remove(self)
        await self.close()

    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        await self.send_json({
            "message": event["message"],
        })

    @database_sync_to_async
    def get_user(self, pk):
        user = LoginUser.objects.get(pk=pk)
        return user

    @database_sync_to_async
    def get_token(self, user):
        return Token.objects.get(user=user).key


# 推送consumer
class PushConsumer(AsyncWebsocketConsumer):
    # chats = dict()

    async def connect(self):
        # headers = dict(self.scope['headers'])
        # sign = headers.get(b'sign').decode() if headers.get(b'sign') else None
        # timestamp = headers.get(b'timestamp').decode() if headers.get(b'timestamp') else None
        self.group_name = self.scope['url_route']['kwargs']['username']
        #
        # if not sign:
        #     self.close()
        #
        # if not timestamp:
        #     self.close()
        #
        # try:
        #     user = await self.get_user()
        #     token = await self.get_token(user)
        #     res = str(str(user.id) + token + timestamp)
        # except LoginUser.DoesNotExist:
        #     self.close()
        #
        # else:
        #     if hashlib.md5(res.encode()).hexdigest() == sign:

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # 创建连接时调用
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        # PushConsumer.chats[self.group_name].remove(self)
        # print(PushConsumer.chats)

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            "data": event['event']
        }))

    @database_sync_to_async
    def get_user(self):
        user = LoginUser.objects.get(username=self.group_name)
        return user

    @database_sync_to_async
    def get_token(self, user):
        return Token.objects.get(user=user).key





