import asyncio

from telegram.ext import Application

from config import get_bot_token
from handlers.callbacks import build_callbacks_handlers
from handlers.messages import build_messages_handlers
from storage.user_state_repository import UserStateRepository


async def main() -> None:
    token = get_bot_token()
    app = Application.builder().token(token).build()

    repo = UserStateRepository()

    for handler in build_messages_handlers(repo):
        app.add_handler(handler)

    for handler in build_callbacks_handlers(repo):
        app.add_handler(handler)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
