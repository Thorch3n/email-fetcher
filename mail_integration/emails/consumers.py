from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EmailProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['channel_name']

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

    async def progress_update(self, event):
        progress = event['progress']
        message = event.get('message', '')

        await self.send(text_data=json.dumps({
            'progress': progress,
            'message': message
        }))
