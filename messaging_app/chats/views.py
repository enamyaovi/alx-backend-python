from django.shortcuts import render
from rest_framework import viewsets, status, filters
from chats.models import Conversation, Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from chats.serializers import (
    RegisterUserSerializer, LoginUserSerializer,  ConversationSerializer,
    MessagesSerializer, UserSerializer)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterUserSerializer
    queryset = get_user_model().objects.all().filter('is_active')

    def get_serializer_class(self, *args, **kwargs): #type:ignore
        if self.action == 'list':
            return UserSerializer
        return self.serializer_class

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.prefetch_related('messages').all()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer
    queryset = Message.objects.prefetch_related('sender').all()
    filter_backends = [filters.OrderingFilter]

@api_view(http_method_names=['POST'])
def get_token(request):
    if request.method == 'POST':
        serializer = LoginUserSerializer(request.data)
        serializer.is_valid()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
