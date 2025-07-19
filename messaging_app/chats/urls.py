from rest_framework.routers import DefaultRouter
from django.urls import path, include
import chats.views as views

NestedDefaultRouter = DefaultRouter()
NestedDefaultRouter.register(r'messages', views.MessagesViewSet, basename='messages')
NestedDefaultRouter.register(r'conversations', views.ConversationViewSet, basename='conversations')

urlpatterns = [
    path('', include(NestedDefaultRouter.urls)),
    path('get_token/', views.get_token, name='get-token')
]