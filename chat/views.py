from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

from accounts.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class ChatRoomListAPIView(APIView):

    def get(self, request):

        rooms = ChatRoom.objects.all()

        serializer = ChatRoomSerializer(
            rooms,
            many=True
        )

        return Response(serializer.data)


class MessageListAPIView(APIView):

    def get(self, request, room_id):

        messages = Message.objects.filter(
            room_id=room_id
        )

        serializer = MessageSerializer(
            messages,
            many=True
        )

        return Response(serializer.data)


class SendMessageAPIView(APIView):

    def post(self, request):

        room_id = request.data.get('room_id')

        sender_id = request.data.get('sender_id')

        content = request.data.get('content')

        message_type = request.data.get(
            'message_type',
            'text'
        )

        try:

            room = ChatRoom.objects.get(id=room_id)

            sender = User.objects.get(id=sender_id)

            message = Message.objects.create(
                room=room,
                sender=sender,
                content=content,
                message_type=message_type,
                status='pending'
            )

            serializer = MessageSerializer(message)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AcceptMessageAPIView(APIView):

    def post(self, request, message_id):

        try:

            message = Message.objects.get(id=message_id)

        except Message.DoesNotExist:

            return Response(
                {"error": "Message not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # already accepted
        if message.status == 'accepted':

            return Response(
                {"error": "Request already accepted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            wholesaler = request.user

        except User.DoesNotExist:

            return Response(
                {"error": "Wholesaler not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        message.status = 'accepted'

        message.accepted_by = wholesaler

        message.save()

        # REAL-TIME UPDATE

        channel_layer = get_channel_layer()

        room_group_name = f'chat_{message.room.id}'

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'product_accepted',
                'message_id': message.id,
                'accepted_by': wholesaler.username,
            }
        )

        serializer = MessageSerializer(message)

        return Response(serializer.data)

class RejectMessageAPIView(APIView):

    def post(self, request, message_id):

        try:

            message = Message.objects.get(
                id=message_id
            )

        except Message.DoesNotExist:

            return Response(
                {"error": "Message not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if message.status == 'rejected':

            return Response(
                {"error": "Request already rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            wholesaler = User.objects.get(id=3)

        except User.DoesNotExist:

            return Response(
                {"error": "Wholesaler not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        message.status = 'rejected'

        message.accepted_by = wholesaler

        message.save()

        serializer = MessageSerializer(
            message
        )

        return Response(
            serializer.data
        )

class WholesalerListAPIView(APIView):

    def get(self, request):

        wholesalers = User.objects.filter(
            role='wholesaler'
        )

        data = []

        for user in wholesalers:

           data.append({

              'id': user.id,

              'username': user.username,

               'is_online': user.is_online,

               'last_seen': user.last_seen,

                'avatar':
                   user.avatar.url
                   if user.avatar
                   else None
            })

        return Response(data)
class CreateDirectRoomAPIView(APIView):

    def post(self, request):

        retailer_id = request.data.get(
            'retailer_id'
        )

        wholesaler_id = request.data.get(
            'wholesaler_id'
        )

        try:

            retailer = User.objects.get(
                id=retailer_id
            )

            wholesaler = User.objects.get(
                id=wholesaler_id
            )

        except User.DoesNotExist:

            return Response(
                {"error": "User not found"},
                status=404
            )

        # check existing room

        rooms = ChatRoom.objects.filter(
            room_type='direct'
        )

        for room in rooms:

            participants = room.participants.all()

            ids = [
                user.id
                for user in participants
            ]

            if sorted(ids) == sorted([
                retailer.id,
                wholesaler.id
            ]):

                serializer = ChatRoomSerializer(
                    room
                )

                return Response(
                    serializer.data
                )

        # create new room

        room = ChatRoom.objects.create(
            room_type='direct'
        )

        room.participants.add(
            retailer,
            wholesaler
        )

        serializer = ChatRoomSerializer(
            room
        )

        return Response(serializer.data)
    
class ChatRoomListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        rooms = ChatRoom.objects.filter(
            participants=request.user
        )

        serializer = ChatRoomSerializer(
            rooms,
            many=True
        )

        return Response(serializer.data)
class CurrentUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "role": request.user.role
        })
class RetailerListAPIView(APIView):

    def get(self, request):

        retailers = User.objects.filter(
            role='retailer'
        )

        data = []

        for user in retailers:

            data.append({

               'id': user.id,

               'username': user.username,

               'is_online': user.is_online,
               'last_seen': user.last_seen,
               'avatar':
                        user.avatar.url
                        if user.avatar
                        else None
            })

        return Response(data)
class LogoutAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        user = request.user

        user.is_online = False

        user.last_seen = timezone.now()

        user.save()

        return Response({
            "message": "Logged out"
        })
class UploadImageAPIView(APIView):

    def post(self, request):

        room_id = request.data.get('room_id')

        sender_id = request.data.get('sender_id')

        image = request.FILES.get('image')

        try:

            room = ChatRoom.objects.get(
                id=room_id
            )

            sender = User.objects.get(
                id=sender_id
            )
            print("IMAGE RECEIVED:", image)
            message = Message.objects.create(

    room=room,

    sender=sender,

    image=image,

    content=request.data.get(
        'content',
        ''
    )
) 
            message.image = image 
            message.save()

            print("SAVED IMAGE:", message.image)

            serializer = MessageSerializer(
                message
            )

            return Response(
                serializer.data
            )

        except Exception as e:

            return Response(
                {'error': str(e)},
                status=400
            )