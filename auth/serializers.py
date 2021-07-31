from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_str, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
from .utils import Util

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class VerifySerializer():
    pass 

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        return {
            "access": user.tokens()["access_token"],
            "refresh": user.tokens()["refresh_token"]
        }

    class Meta:
        model = User
        fields = ["email", "password", "username", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = authenticate(email=email, password=password)

        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email).provider != "email":
                raise AuthenticationFailed(f"You should login with {user.provider}")

        if not user:
            raise AuthenticationFailed("Invalid credentials.")
        
        if not user.is_verified:
            raise AuthenticationFailed("Account not verified.")


        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens
        }
        return super().validate(attrs)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    redirect_url = serializers.CharField(max_length=200)

    class Meta:
        fields = ["email"]
    
class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Password reset token not valid.")

            user.set_password(password)
            user.save()

            return user
        except:
            raise AuthenticationFailed("Password reset token not valid.")
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(min_length=1)

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid token")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["currency", "username"]