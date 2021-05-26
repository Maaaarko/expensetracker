from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from auth.models import User

import random

import environ
env = environ.Env()
environ.Env.read_env("./expensetracker/.env")


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)

def register_social(provider, id, email, name):
    

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)

        if user.provider == provider:
            user = authenticate(email=email, password=env("SECRET_KEY"))

            tokens = user.tokens()

            return {
                "username": user.username,
                "email": user.email,
                "tokens": {
                    "access": tokens["access_token"],
                    "refresh": tokens["refresh_token"]
                }
            }

        else:
            raise AuthenticationFailed({"detail": f"You should login with {user.provider}, not with your Google account."})

    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "password": env("SECRET_KEY")
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.provider = provider
        user.save()

        user = authenticate(email=email, password=env("SECRET_KEY"))

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens()
        }