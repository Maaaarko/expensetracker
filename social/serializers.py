from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . import google
from .register import register_social

import environ
env = environ.Env()
environ.Env.read_env("./expensetracker/.env")

class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        data = google.Google.validate(auth_token)
        try:
            user["sub"]
        except:
            raise serializers.ValidationError("Invalid token.")

        if data["aud"] != env("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed("Invalid token.")

        id = data["sub"]
        email = data["email"]
        name = data["name"]
        provider = "google"

        return register_social(provider=provider, id=id, email=email, name=name)
