from django.core.mail import EmailMessage
from rest_framework import renderers

import threading

class EmailThread(threading.Thread):
    def __init__(self, message):
        self.email = message
        threading.Thread.__init__(self)

        def run(self):
            self.email.send()

class Util:
    @staticmethod
    def send_mail(data):
        message = EmailMessage(subject=data["subject"], body=data["body"], to=[data["to"]])
        message.send()

        EmailThread(message).start()