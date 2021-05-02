from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from auth.models import User

import environ
env = environ.Env()
environ.Env.read_env("./expensetracker/.env")

def register_social(provider, id, email, name):
    
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)

        if user.provider == provider:
            user = authenticate(email=email, password=env("SECRET_KEY"))

            return {
                "username": user.username,
                "email": user.email,
                "tokens": user.tokens()
            }

        else:
            raise AuthenticationFailed(f"You should login with {user.provider}")

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