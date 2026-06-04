from django.contrib import admin
from django.urls import path, include
from accounts.custom_jwt import (
    CustomTokenObtainPairView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/chat/', include('chat.urls')),
    
    path(
    'api/token/',
    CustomTokenObtainPairView.as_view()
    ),

    path(
    'api/token/refresh/',
    TokenRefreshView.as_view()
    ),
    path(
    'api/accounts/',
    include('accounts.urls')
    ),
    
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)