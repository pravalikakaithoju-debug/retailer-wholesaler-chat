from django.db import models
from django.conf import settings


class ChatRoom(models.Model):

    ROOM_TYPES = (
        ('direct', 'Direct'),
        ('broadcast', 'Broadcast'),
    )

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.room_type} - {self.id}"


class Message(models.Model):

    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('product_request', 'Product Request'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('accepted', 'Accepted'),
    )

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    message_type = models.CharField(
        max_length=30,
        choices=MESSAGE_TYPES,
        default='text'
    )

    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_messages'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.content[:30]