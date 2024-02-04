from django.urls import path
from .views import ChatList, MessageList


urlpatterns = [
    path('api/v1/chats/', ChatList.as_view()),
    path('api/v1/chats/<int:chat_id>/messages/', MessageList.as_view())
]