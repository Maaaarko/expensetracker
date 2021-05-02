import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, PasswordResetSerializer, PasswordChangeSerializer
from .utils import Util

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):    
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data["email"])
        token = RefreshToken.for_user(user)
        domain = get_current_site(request).domain 
        relative = reverse("verify")
        
        url = f"http://{domain}{relative}?token={str(token.access_token)}"

        email_payload = {
            "body": url,
            "subject": "Verify your account",
            "to": user.email 
        }
        Util.send_mail(email_payload)

        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

class VerifyView(generics.GenericAPIView):

    def get(self, request):
        token = request.GET["token"]
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=data["user_id"])
            if not user.is_verified: 
                user.is_verified = True
                user.save()
            return Response({"message": "Account verified."}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"error": "Token invalid."}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):

        email = request.data["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            domain = get_current_site(request).domain 
            relative = reverse("token_reset", kwargs={"uidb64": uidb64, "token": token})
            
            url = f"http://{domain}{relative}"

            email_payload = {
                "body": url,
                "subject": "Reset your password",
                "to": user.email 
            }
            Util.send_mail(email_payload)

        return Response({"message": "Reset email sent."}, status=status.HTTP_200_OK)

class PasswordTokenView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Password reset token not valid."})

            return Response({"message": "Token valid.", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({"error": "Password reset token not valid."}) 

class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({"message": "Password changed."}, status=status.HTTP_200_OK)
