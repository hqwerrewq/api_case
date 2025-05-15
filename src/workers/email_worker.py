import asyncio
import json
from typing import Dict, Any

from src.core.redis import redis_client
from src.core.config import settings
from src.services.email import EmailService


async def process_email_queue():
    while True:
        try:
            task_json = await redis_client.blpop(settings.redis.EMAIL_QUEUE_NAME, timeout=30)

            if task_json:
                queue_name, task_data = task_json
                task: Dict[str, Any] = json.loads(task_data)

                if task["type"] == "welcome_email":
                    await EmailService.send_welcome_email(task["email"])
        except json.JSONDecodeError as e:
            await asyncio.sleep(1)
        except Exception as e:
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(process_email_queue())