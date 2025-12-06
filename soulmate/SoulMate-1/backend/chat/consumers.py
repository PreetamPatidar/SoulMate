import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Authenticate user from token in query params
        token = self.scope['query_string'].decode().split('token=')[1] if 'token=' in self.scope['query_string'].decode() else None
        if not token:
            await self.close()
            return

        # In production, validate JWT token here
        # For now, assume token is user_id (simplified)
        try:
            self.user = await self.get_user_from_token(token)
            if not self.user:
                await self.close()
                return
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            await self.close()
            return

        # Check if user is participant in the room
        if not await self.is_user_in_room(self.user, self.room_id):
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Update online status
        await self.update_online_status(self.user, True)

        logger.info(f"User {self.user.email} connected to room {self.room_id}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Update online status
        if hasattr(self, 'user'):
            await self.update_online_status(self.user, False)

        logger.info(f"User {self.user.email if hasattr(self, 'user') else 'unknown'} disconnected from room {self.room_id}")

    async def receive_json(self, content):
        message_type = content.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(content)
        elif message_type == 'typing_indicator':
            await self.handle_typing_indicator(content)
        elif message_type == 'read_receipt':
            await self.handle_read_receipt(content)
        else:
            logger.warning(f"Unknown message type: {message_type}")

    async def handle_chat_message(self, content):
        try:
            message_content = content.get('message')
            message_type = content.get('message_type', 'text')
            file_url = content.get('file_url')

            if not message_content:
                await self.send_json({'error': 'Message content is required'})
                return

            # Save message to database
            message = await self.save_message(
                self.user, self.room_id, message_content, message_type, file_url
            )

            # Broadcast message to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'sender': {
                            'id': self.user.id,
                            'email': self.user.email,
                            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
                        },
                        'content': message.content,
                        'timestamp': message.timestamp.isoformat(),
                        'message_type': message.message_type,
                        'file_url': message.file_url,
                    }
                }
            )
        except Exception as e:
            logger.error(f"Error handling chat message: {e}")
            await self.send_json({'error': 'Failed to send message'})

    async def handle_typing_indicator(self, content):
        is_typing = content.get('is_typing', False)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': self.user.id,
                'is_typing': is_typing,
            }
        )

    async def handle_read_receipt(self, content):
        message_ids = content.get('message_ids', [])

        await self.mark_messages_as_read(message_ids, self.user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'read_receipt',
                'user_id': self.user.id,
                'message_ids': message_ids,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send_json({
            'type': 'chat_message',
            'message': event['message']
        })

    async def typing_indicator(self, event):
        await self.send_json({
            'type': 'typing_indicator',
            'user_id': event['user_id'],
            'is_typing': event['is_typing']
        })

    async def read_receipt(self, event):
        await self.send_json({
            'type': 'read_receipt',
            'user_id': event['user_id'],
            'message_ids': event['message_ids']
        })

    @database_sync_to_async
    def get_user_from_token(self, token):
        # Simplified: in production, decode JWT
        try:
            user_id = int(token)
            return User.objects.get(id=user_id)
        except (ValueError, User.DoesNotExist):
            return None

    @database_sync_to_async
    def is_user_in_room(self, user, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
            return user in room.participants.all()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, room_id, content, message_type, file_url):
        room = ChatRoom.objects.get(id=room_id)
        return Message.objects.create(
            sender=user,
            chat_room=room,
            content=content,
            message_type=message_type,
            file_url=file_url
        )

    @database_sync_to_async
    def update_online_status(self, user, status):
        user.online_status = status
        user.save()

    @database_sync_to_async
    def mark_messages_as_read(self, message_ids, user):
        Message.objects.filter(id__in=message_ids, chat_room__participants=user).update(is_read=True)
