from rest_framework import serializers
from .models import Conversation, Message
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'password',
            'role',
            'phone_number'
            ]
        # extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = [
            'role'
        ]

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = [
            'user_id'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserTokenSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users and return Token
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self,obj):
        try:    
            user = authenticate(
                username= obj.get('username'),
                password=obj.get('password')
            )
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return token.key
        except AuthenticationFailed:
            raise

    def validate(self, attrs):
        s = authenticate(
            username=attrs['username'],
            password=attrs['password']
            )
        if s is None:
            raise AuthenticationFailed("{'error':'Wrong username or password'}")
        return super().validate(attrs)
        

class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = [
            'sender',
            'message_body',
            'sent_at',
            'conversation'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def get_sender(self, obj):
        return obj.sender.email

class UserLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserLimitedSerializer(many=True, read_only=True)
    messages = MessagesSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages'
        ]

class CreateChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            'participants'
        ]
    
    def validate(self, attrs):
        user = self.context['request'].user
        participants = attrs.get('participants', [])
        if user not in participants:
            participants.append(user)
        attrs['participants'] = participants
        if len(attrs.get('participants')) < 2:
            raise serializers.ValidationError("Chat Room must have more than 1 User")
        return attrs

class ChatRoomListSerializer(serializers.ModelSerializer):
    participants = UserLimitedSerializer(many=True)
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants'
        ]
        read_only_fields = [
            'conversation_id',
            'participants'
        ]

