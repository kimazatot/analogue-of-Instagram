from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer, MessagesSerializer
from .models import Chat, Messages


class ChatList(APIView):
    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(participants=user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save()
            chat.participants.add(request.user)
            return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageList(APIView):

    def post(self, request):
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            chat = Chat.objects.get(id=request.data.get('chat'))
            if chat.participants.filter(id=request.user.id).exists():
                message = serializer.save(sender=request.user, chat=chat)
                return Response(MessagesSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        if chat.participants.filter(id=request.user.id).exists(): #
            messages = chat.messages.all()
            serializer = MessagesSerializer(messages, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)