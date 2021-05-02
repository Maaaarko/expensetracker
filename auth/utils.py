from django.core.mail import EmailMessage
from rest_framework import renderers

class Util:
    @staticmethod
    def send_mail(data):
        message = EmailMessage(subject=data["subject"], body=data["body"], to=[data["to"]])
        message.send()
