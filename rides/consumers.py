from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync, sync_to_async
from rides.models import Ride
from django_redux import action, AsyncReduxConsumer
import json

from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
User = get_user_model()


class MyConsumer(WebsocketConsumer):

    # Function to connect to the websocket
    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:

            self.group_name = str(self.scope["user"].pk)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    # Function to disconnet the Socket
    def disconnect(self, close_code):
        self.close()
        # pass

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        # print(event)
        self.send(text_data=json.dumps(event["text"]))

    def addRequests(self, event):
        # print(event)
        self.send(text_data=json.dumps(event))

    def removeRequests(self, event):
        # print(event)
        self.send(text_data=json.dumps(event))

    def removeMYRequests(self, event):
        # print(event)
        self.send(text_data=json.dumps(event))

    def updateRequests(self, event):
        # print(event)
        self.send(text_data=json.dumps(event))

    def sendNotification(self, event):
        self.send(text_data=json.dumps(event))