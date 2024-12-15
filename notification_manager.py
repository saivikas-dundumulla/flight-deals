import os
import dotenv
from twilio.rest import Client

class NotificationManager:
    def __init__(self):
        dotenv.load_dotenv(dotenv_path=".env")
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.getenv("AUTH_TOKEN")
        self._from = os.getenv("FROM")
        self.to = os.getenv("TO")

    def send_sms(self, subject:str, body:str):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=f"{subject}\n\n{body}",
            from_= self._from,
            to= self.to
        )
        print(message.status)