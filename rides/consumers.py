from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from rides.models import Request, Ride
from django_redux import action, AsyncReduxConsumer
import json
User = get_user_model()


# @database_sync_to_async
# def get_user():
#     user = get_object_or_404(User, pk=1)
#     print(user)
#     return user


class MyConsumer(AsyncReduxConsumer):

    async def connect(self):
        await super().connect()
        print(self.scope['user'])
        # if self.user is not None and self.user.is_authenticated:
        #     await self.send_json({
        #         'type': 'SET_USER',
        #         'user': {
        #             'username': self.user.username,
        #         }
        #     })
        # else:
        # get all requests
        # requests = await getRequests(self)
        # print(requests)
        # await self.send_json({
        #     'type': 'SET_USER',
        #     'user': {
        #         'requests': json.dumps(requests),
        #     }
        # })

    async def disconnect(self, code):
        await super().disconnect(code)
        await self.close()
        print('disconnect', code)




@database_sync_to_async
def getRequests(self):
    rides = Ride.objects.all().filter(uploader=self.user)
    print(rides)
    qs = []
    for ride in rides:
        qs += ride.request.all()
    return qs


# class RideConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         # ridePK = self.scope['url_route']['kwargs']['pk']
#         user = self.scope['user']
#
#         if not user.is_authenticated:
#             # await self.close()
#             user = get_user()
#         print(user)
#
#         await self.accept()
#
#     async def receive_json(self, content, **kwargs):
#         action_type = content.get('type')
#
#         if action_type == 'echo.message':
#             await self.send_json({
#                 'type': action_type,
#                 'data': content.get('data'),
#             })
#         elif action_type == 'join':
#             data = content.get('ride')
#
#
#
#         else:
#             print('skata')
#
#
#
#
#     async def disconnect(self, code):
#         await super().disconnect(code)
