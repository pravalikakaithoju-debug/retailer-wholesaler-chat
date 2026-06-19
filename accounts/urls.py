from django.urls import path

from .views import *

from .views import (
    UploadAvatarAPIView,RegisterAPIView,ForgotPasswordAPIView,ResetPasswordAPIView,ForgotUsernameAPIView
)


urlpatterns = [

    path(
        'upload-avatar/',
        UploadAvatarAPIView.as_view()
    ),
    path(
    'register/',
    RegisterAPIView.as_view()
),
path(
    'forgot-password/',
    ForgotPasswordAPIView.as_view()
),
path(
    'reset-password/',
    ResetPasswordAPIView.as_view()
),
path(
    'forgot-username/',
    ForgotUsernameAPIView.as_view()
),
    
]