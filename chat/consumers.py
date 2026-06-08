import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, Message
from accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope['url_route']['kwargs']['room_id']

        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)
        print("MESSAGE RECEIVED")
        print(data)
        message = data['message']
        sender_id = data['sender_id']

        room = await self.get_room(self.room_id)

        sender = await self.get_user(sender_id)

        saved_message = await self.save_message(
            room,
            sender,
            message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved_message.content,
                'sender': sender.username,
                'message_id': saved_message.id,
            }
        )


    async def chat_message(self, event):

        await self.send(text_data=json.dumps({

            'type': 'chat_message',

            'message': event['message'],

            'sender': event['sender'],

            'message_id': event['message_id'],
        }))

    async def product_accepted(self, event):

        await self.send(text_data=json.dumps({

            'type': 'product_accepted',

            'message_id': event['message_id'],

            'accepted_by': event['accepted_by'],

            'status': 'accepted'
        }))

    @database_sync_to_async
    def get_room(self, room_id):

        return ChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def get_user(self, user_id):

        return User.objects.get(id=user_id)

    @database_sync_to_async
    def save_message(self, room, sender, content):

        return Message.objects.create(
            room=room,
            sender=sender,
            content=content,
            message_type='text',
            status='pending'
        )