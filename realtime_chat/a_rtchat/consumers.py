from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

from .models import *
import json



class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user'] #request no longer available so user scope from the Authmiddlewarestack
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] #kwargs is an array of arguments with keys and values
                                                                                #This KWARG was in the routing.py
        self.chatroom = get_object_or_404(ChatGroup, group_name = self.chatroom_name)
        """
        Bridge gap between sync and async
        Option 1:    
            class x(AsyncWebsocketConsumer)
                async def function()
                    await self.accept()
        Option 2:
            async_to_sync(self.channel_layer.group_add)()
        
        """
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name #Channel name is unique id ish thing
        )

        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,self.channel_name
        )

        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

    def receive(self, text_data):
        #text_data is json
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        if (body == "Clear"):
            GroupMessage.objects.filter(group=self.chatroom).delete()
            # (group=self.chatroom)

        #Adding the message into the thing
        message = GroupMessage.objects.create(
            body = body,
            author = self.user,
            group = self.chatroom
        )
        event = { #Dictionary Def with key and value
            'type': 'message_handler', #Says with function it should handle!
            'message_id': message.id,
        }
        
        async_to_sync(self.channel_layer.group_send)(
           self.chatroom_name, event 
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message' : message,
            'user': self.user,
            'chat_group': self.chatroom,
        }
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context = context)
        self.send(text_data=html)
    
    def update_online_count(self):
        online_count = self.chatroom.users_online.count()

        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    
    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string("a_rtchat/partials/online_count.html", {'online_count': online_count})
        self.send(text_data=html)
        
    
