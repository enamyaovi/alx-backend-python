from rest_framework import serializers
from .models import Conversation, Message
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'role'
            ]
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = [
            'role'
        ]

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginUserSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users and return Token
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return {'email':email, 'token':token.key}
        raise serializers.ValidationError(
            'A user with this email and password was not found.')

class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(method_name='get_sender')
    class Meta:
        model = Message
        fields = [
            'sender',
            'message_body',
            'sent_at'
        ]

    def get_sender(self, obj):
        return obj.sender.email


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessagesSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages'
        ]