from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response



User = get_user_model()

class RegisterAPIView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def post(self, request):

        User = get_user_model()

        username = request.data.get(
            'username'
        )

        password = request.data.get(
            'password'
        )

        role = request.data.get(
            'role'
        )
        email = request.data.get(
    'email'
)

        avatar = request.FILES.get(
            'avatar'
        )

        if User.objects.filter(
            username=username
        ).exists():

            return Response(
                {
                    "error":
                    "Username already exists"
                },
                status=400
            )

        user = User.objects.create_user(
    username=username,
    password=password,
    role=role,
    email=email
)

        if avatar:

            user.avatar = avatar
            user.save()

        return Response({

            "message":
            "Registration successful",

            "username":
            user.username

        })

class ForgotPasswordAPIView(APIView):

    def post(self, request):

        email = request.data.get(
            'email'
        )

        new_password = request.data.get(
            'new_password'
        )

        User = get_user_model()

        try:

            user = User.objects.filter(
    email=email
).first()
            if not user:

                return Response(
        {"error": "Email not found"},
        status=400
    )

            user.set_password(
                new_password
            )

            user.save()

            return Response({
                "message":
                "Password updated successfully"
            })

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "Email not found"
                },
                status=400
            )
class ResetPasswordAPIView(APIView):

    def post(self, request):

        user_id = request.data.get(
            'user_id'
        )

        token = request.data.get(
            'token'
        )

        password = request.data.get(
            'password'
        )

        user = User.objects.get(
            id=user_id
        )

        if not (
            default_token_generator
            .check_token(
                user,
                token
            )
        ):

            return Response(
                {
                    "error":
                    "Invalid token"
                },
                status=400
            )

        user.set_password(
            password
        )

        user.save()

        return Response({
            "message":
            "Password updated"
        })
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
class ForgotUsernameAPIView(APIView):

    def post(self, request):

        email = request.data.get(
            'email'
        )

        User = get_user_model()

        try:

            user = User.objects.filter(
                email=email
            ).first()

            if not user:

                return Response(
                    {
                        "error":
                        "Email not found"
                    },
                    status=400
                )

            return Response({

                "username":
                user.username

            })

        except Exception as e:

            return Response(
                {
                    "error":
                    str(e)
                },
                status=400
            )
