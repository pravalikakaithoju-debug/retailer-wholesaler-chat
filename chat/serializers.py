from rest_framework import serializers

from .models import ChatRoom, Message
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'role','is_online','avatar',]


class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)

    accepted_by = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):

    participants = UserSerializer(
        many=True,
        read_only=True
    )

    messages = MessageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ChatRoom
        fields = '__all__'
