from src.core.redis import redis_client
from src.core.config import settings
import json

class EmailService:
    @staticmethod
    async def send_welcome_email(email: str):
        message = f"Sending welcome email to {email}"
        with open("email.log", "a") as f:
            f.write(message + "\n")

    @staticmethod
    async def enqueue_email_task(email: str) -> None:
        task = {
            "type": "welcome_email",
            "email": email,
            "message": "Welcome to our service!"
        }
        await redis_client.rpush(settings.redis.EMAIL_QUEUE_NAME, json.dumps(task))