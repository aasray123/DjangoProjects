from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import *
import json



class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user'] #request no longer available so user scope from the Authmiddlewarestack
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] #kwargs is an array of arguments with keys and values
                                                                                #This KWARG was in the routing.py
        self.chatroom = get_object_or_404(ChatGroup, group_name = self.chatroom_name)

        self.channel_layer.group_add(
            self.chatroom_name, self.channel_name #Channel name is unique id ish thing
        )

        self.accept()

    def receive(self, text_data):
        #text_data is json
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        #Adding the message into the thing
        message = GroupMessage.objects.create(
            body = body,
            group = self.chatroom,
            author = self.user

        )
        context = {
            'message' : message,
            'user': self.user,
        }
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context = context)
        self.send(text_data=html)