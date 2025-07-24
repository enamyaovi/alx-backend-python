from django.shortcuts import render
from rest_framework import viewsets, status, filters
from chats.models import Conversation, Message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model, logout
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token

from django_filters import rest_framework as d_filters

from chats.serializers import (
    RegisterUserSerializer, UserTokenSerializer,  ConversationSerializer,
    MessagesSerializer, UserSerializer, ChatRoomListSerializer, CreateChatRoomSerializer)

from chats.permissions import IsParticipantOfConversation, IsAnonOrAdminUser
from chats.pagination import MessageListingPagination
from chats.filters import MessageFilter

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterUserSerializer
    queryset = get_user_model().objects.all()
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAnonOrAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs): #type:ignore
        if self.action == 'list':
            return UserSerializer
        return self.serializer_class

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.prefetch_related('participants').all()
    # permission_classes = [IsParticipantOfConversation]

    def get_serializer_class(self): # type: ignore
        if self.action == 'list':
            return ChatRoomListSerializer
        elif self.action == 'create':
            return CreateChatRoomSerializer
        return super().get_serializer_class()
    

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer
    queryset = Message.objects.prefetch_related('sender').all()
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter, d_filters.DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessageListingPagination

    def get_queryset(self): # type: ignore
        if self.action in ['list','update','delete']:
            return Message.objects.all().filter(sender=self.request.user)
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer
        obj = serializer(data=request.data)
        self.check_object_permissions(request, obj, *args, **kwargs)
        return super().create(request, *args, **kwargs)


@api_view(http_method_names=['POST', 'GET'])
@permission_classes([AllowAny])
def get_token(request):
    if request.method == 'POST':
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
    return Response(
        data={
            "message":"Only 'POST' method allowed. Send your {'username':'password'} to retrieve your token"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(http_method_names=['POST'])
def log_out(request):
    if request.method == 'POST':
        try:
            Token.objects.get(user=request.user).delete()
        except Token.DoesNotExist:
            pass
        logout(request)
        return Response({"message":"User Logged Out Successfully"}, status=status.HTTP_200_OK)
