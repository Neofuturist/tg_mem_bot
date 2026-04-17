import os

from dotenv import load_dotenv


load_dotenv()


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError(
            "BOT_TOKEN is not set. Please set BOT_TOKEN in environment or .env file before running the bot."
        )
    return token
