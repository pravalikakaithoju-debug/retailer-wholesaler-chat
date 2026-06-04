from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UploadAvatarAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        user = request.user

        avatar = request.FILES.get(
            'avatar'
        )

        if not avatar:

            return Response({
                "error":
                "No image uploaded"
            }, status=400)

        user.avatar = avatar

        user.save()

        return Response({

            "message":
            "Avatar uploaded",

            "avatar_url":
            user.avatar.url
        })