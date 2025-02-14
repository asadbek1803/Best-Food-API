import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from .models import Delivery

class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.room_group_name = f"order_{self.order_id}"

        try:
            # Buyurtmaning mavjudligini tekshiramiz
            delivery = await self.get_delivery(self.order_id)
            if not delivery:
                await self.close()
                return

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

        except ObjectDoesNotExist:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Haydovchining joylashuvini bazaga saqlaymiz
        delivery = await self.get_delivery(self.order_id)
        if delivery:
            delivery.location_latitude = latitude
            delivery.location_longitude = longitude
            await self.save_delivery(delivery)

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

    @staticmethod
    async def get_delivery(order_id):
        try:
            return Delivery.objects.get(order_id=order_id)
        except Delivery.DoesNotExist:
            return None

    @staticmethod
    async def save_delivery(delivery):
        delivery.save()
