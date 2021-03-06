from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("verify/", views.VerifyView.as_view(), name="verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset/", views.PasswordResetView().as_view(), name="reset"),
    path("reset/<uidb64>/<token>/", views.PasswordTokenView().as_view(), name="token_reset"),
    path("set-password/", views.PasswordChangeView.as_view(), name="change-password"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]