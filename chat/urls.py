from django.urls import path

from .views import (
    ChatRoomListAPIView,
    MessageListAPIView,
    SendMessageAPIView,
    AcceptMessageAPIView,
    RejectMessageAPIView,
    WholesalerListAPIView,
    CreateDirectRoomAPIView,
    CurrentUserAPIView,
    RetailerListAPIView,
    LogoutAPIView,
    UploadImageAPIView,
    DeleteChatAPIView,
    AcceptedProductsAPIView,
    DeleteAcceptedProductAPIView

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
    'reject-message/<int:message_id>/',
    RejectMessageAPIView.as_view()
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
    path(
    'logout/',
    LogoutAPIView.as_view()
    ), 
    path(
    'upload-image/',
    UploadImageAPIView.as_view()
    ), 
    path(
    'delete-chat/<int:room_id>/',
    DeleteChatAPIView.as_view()
),
path(
    'accepted-products/',
    AcceptedProductsAPIView.as_view()
),
path(
    'delete-accepted-product/<int:product_id>/',
    DeleteAcceptedProductAPIView.as_view()
),

]