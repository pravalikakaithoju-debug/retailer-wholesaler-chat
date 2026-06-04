from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


class CustomTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    def validate(self, attrs):

        data = super().validate(attrs)

        self.user.is_online = True
        self.user.save()

        return data


class CustomTokenObtainPairView(
    TokenObtainPairView
):

    serializer_class = (
        CustomTokenObtainPairSerializer
    )