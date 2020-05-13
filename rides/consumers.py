from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404

User = get_user_model()

@database_sync_to_async
def get_user():
    user = get_object_or_404(User, pk=1)
    print(user)
    return user




class RideConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # ridePK = self.scope['url_route']['kwargs']['pk']
        user = self.scope['user']

        if not user.is_authenticated:
            # await self.close()
            user = get_user()
        print(user)

        await self.accept()

    async def receive_json(self, content, **kwargs):
        action_type = content.get('type')

        if action_type == 'echo.message':
            await self.send_json({
                'type': action_type,
                'data': content.get('data'),
            })
        elif action_type == 'join':
            data = content.get('ride')



        else:
            print('skata')




    async def disconnect(self, code):
        await super().disconnect(code)




