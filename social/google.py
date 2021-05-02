from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    @staticmethod
    def validate(auth_token):
        try:
            id = id_token.verify_oauth2_token(auth_token, requests.Request())

            if "accounts.google.com" in id["iss"]:
                return id
        
        except:
            return ("Invalid token")