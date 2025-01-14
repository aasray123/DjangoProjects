from django.urls import path

#Consumers is like a views for websockets
from .consumers import *


websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()) #Chatroom_name is in the model
    
]