import requests
import asyncio
import traceback

from bday import settings
from bday import state
from bday.gcal import CalendarClient
from bday.commands import Commands
from bday.telegram import Telegram, TelegramBotMessage, SkipTelegramMessage, InvalidBotCommand


class TelegramListener:
    def __init__(self):
        self.gcal = CalendarClient()
        self.telegram = Telegram()
        self.send = self.telegram.send
        self.updates_url = f"{settings.TELEGRAM_BASE_URL}/getUpdates?"

    def handle_update(self, update):
        try:
            message = TelegramBotMessage(update)
        except InvalidBotCommand:
            self.telegram.send("Sorry I don't get that")
            return
        except SkipTelegramMessage:
            return

        Commands.get(
            command=message.command, args=message.args, telegram=Telegram(message.chat_id)
        ).call()

    async def get_updates(self):
        offset = state.offset.get("offset")
        query = f"offset={offset + 1}" if offset is not None else ""
        response = requests.get(self.updates_url + query)

        if response.json()["ok"]:
            for r in response.json()["result"]:
                state.offset["offset"] = r["update_id"]
                return r

    async def listen(self):
        while True:
            await asyncio.sleep(1)
            try:
                update = await self.get_updates() or {}
                self.handle_update(update)
            except:
                traceback.print_exc()


async def main():
    telegram = TelegramListener()
    # telegram.send("Server started")
    await asyncio.gather(telegram.listen())


if __name__ == "__main__":
    print("Let's go")
    asyncio.run(main())
