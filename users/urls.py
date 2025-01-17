from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "reset-password-request/",
        PasswordResetRequestAPIView.as_view(),
        name="reset_password_request",
    ),
    path(
        "reset-password-confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="reset_password_confirm",
    ),
]
