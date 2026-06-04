from django.urls import path

from .views import (
    UploadAvatarAPIView
)

urlpatterns = [

    path(
        'upload-avatar/',
        UploadAvatarAPIView.as_view()
    ),
]