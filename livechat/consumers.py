import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.timezone import localtime
from .models import Room, Message


# Development uchun oddiy in-memory online user store
ONLINE_USERS = {}  # {room_name: set([username1, username2, ...])}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        session = self.scope.get("session")
        self.username = "Anonymous"

        if session:
            self.username = session.get("chat_username", "Anonymous").strip() or "Anonymous"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.add_online_user(self.room_name, self.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "presence_update",
            }
        )

    async def disconnect(self, close_code):
        await self.remove_online_user(self.room_name, self.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "presence_update",
            }
        )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type", "message")

        if event_type == "typing":
            is_typing = data.get("is_typing", False)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_status",
                    "username": self.username,
                    "is_typing": is_typing,
                    "sender_channel_name": self.channel_name,
                }
            )
            return

        if event_type == "message":
            message = data.get("message", "").strip()
            if not message:
                return

            saved = await self.save_message(self.room_name, self.username, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": saved["content"],
                    "username": saved["username"],
                    "created_at": saved["created_at"],
                }
            )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": event["message"],
                    "username": event["username"],
                    "created_at": event["created_at"],
                }
            )
        )

    async def typing_status(self, event):
        # o'zi yuborgan typing eventni o'ziga qaytarmaymiz
        if event.get("sender_channel_name") == self.channel_name:
            return

        await self.send(
            text_data=json.dumps(
                {
                    "type": "typing",
                    "username": event["username"],
                    "is_typing": event["is_typing"],
                }
            )
        )

    async def presence_update(self, event):
        users = await self.get_online_users(self.room_name)

        await self.send(
            text_data=json.dumps(
                {
                    "type": "presence",
                    "count": len(users),
                    "users": users,
                }
            )
        )

    @sync_to_async
    def save_message(self, room_name, username, message):
        room, _ = Room.objects.get_or_create(name=room_name)
        msg = Message.objects.create(
            room=room,
            username=username,
            content=message,
        )

        return {
            "username": msg.username,
            "content": msg.content,
            "created_at": localtime(msg.created_at).strftime("%H:%M"),
        }

    @sync_to_async
    def add_online_user(self, room_name, username):
        if room_name not in ONLINE_USERS:
            ONLINE_USERS[room_name] = set()
        ONLINE_USERS[room_name].add(username)

    @sync_to_async
    def remove_online_user(self, room_name, username):
        if room_name in ONLINE_USERS:
            ONLINE_USERS[room_name].discard(username)
            if not ONLINE_USERS[room_name]:
                del ONLINE_USERS[room_name]

    @sync_to_async
    def get_online_users(self, room_name):
        return sorted(list(ONLINE_USERS.get(room_name, set())))