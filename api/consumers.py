import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.room_group_name = f"order_{self.order_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data["latitude"]
        longitude = data["longitude"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "location_update",
                "latitude": latitude,
                "longitude": longitude,
            },
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event))
