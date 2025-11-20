from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

User = get_user_model()

class DeliveryLocationConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for delivery location streaming.

    Expected messages from delivery app:
      { "type": "location", "order_id": 123, "lat": 12.34, "lng": 56.78 }

    Behavior:
    - Broadcasts location updates to group "order_<order_id>"
    - Any clients subscribed to that group (customer frontends) will receive updates
    """

    async def connect(self):
        user = self.scope.get('user')
        # Optionally restrict to authenticated users only:
        # if user is None or user.is_anonymous:
        #     await self.close()
        await self.accept()

    async def receive_json(self, content, **kwargs):
        """
        Handle incoming JSON messages.
        """
        msg_type = content.get('type')
        if msg_type == 'location':
            order_id = content.get('order_id')
            lat = content.get('lat')
            lng = content.get('lng')

            if order_id is None or lat is None or lng is None:
                # malformed payload
                await self.send_json({'error': 'order_id, lat, lng required for location messages'})
                return

            group_name = f'order_{order_id}'

            # Broadcast to group
            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'location.update',
                    'lat': lat,
                    'lng': lng,
                    'sender': getattr(self.scope.get('user'), 'id', None),
                }
            )

            # Optionally persist to DB/Redis asynchronously (not implemented here)

        elif msg_type == 'subscribe':
            # allow clients to subscribe to an order group to receive updates
            order_id = content.get('order_id')
            if order_id is None:
                await self.send_json({'error': 'order_id required to subscribe'})
                return
            group_name = f'order_{order_id}'
            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.send_json({'subscribed': order_id})

        elif msg_type == 'unsubscribe':
            order_id = content.get('order_id')
            if order_id is None:
                await self.send_json({'error': 'order_id required to unsubscribe'})
                return
            group_name = f'order_{order_id}'
            await self.channel_layer.group_discard(group_name, self.channel_name)
            await self.send_json({'unsubscribed': order_id})

        else:
            await self.send_json({'error': 'unknown message type'})

    async def location_update(self, event):
        """
        Handler for group messages of type 'location.update'.
        """
        await self.send_json({
            'type': 'location',
            'lat': event.get('lat'),
            'lng': event.get('lng'),
            'sender': event.get('sender'),
        })

    async def disconnect(self, close_code):
        # Optionally remove from all groups (Channels removes automatically on socket close)
        return None
