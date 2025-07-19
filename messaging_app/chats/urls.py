from rest_framework.routers import DefaultRouter
from django.urls import path, include
from chats.views import MessageViewSet, ConversationViewSet, get_token

NestedDefaultRouter = DefaultRouter()
NestedDefaultRouter.register(r'messages', MessageViewSet, basename='messages')
NestedDefaultRouter.register(r'conversations', ConversationViewSet, basename='conversations')

urlpatterns = [
    path('', include(NestedDefaultRouter.urls)),
    path('get_token/', get_token, name='get-token')
]