from django.urls import path

from .views import (
    ChatRoomListAPIView,
    MessageListAPIView,
    SendMessageAPIView,
    AcceptMessageAPIView,
    WholesalerListAPIView,
    CreateDirectRoomAPIView,
    CurrentUserAPIView,
    RetailerListAPIView,

)

urlpatterns = [

    path(
        'rooms/',
        ChatRoomListAPIView.as_view()
    ),

    path(
        'messages/<int:room_id>/',
        MessageListAPIView.as_view()
    ),

    path(
        'send-message/',
        SendMessageAPIView.as_view()
    ),
    path(
    'accept-message/<int:message_id>/',
    AcceptMessageAPIView.as_view()
    ),
    path(
    'wholesalers/',
    WholesalerListAPIView.as_view()
    ),
    path(
    'create-direct-room/',
    CreateDirectRoomAPIView.as_view()
    ),
    path(
    'current-user/',
    CurrentUserAPIView.as_view()
    ),
    path(
    'retailers/',
    RetailerListAPIView.as_view()
),
]