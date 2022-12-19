import requests
import asyncio
import json
import traceback
import re

from bday import settings
from bday import state
from bday.gcal import CalendarClient

HELP = """
/ping - Check alive
/upcoming - Show upcoming bdays
/add - Add new bday (e.g. 2022-01-01 Harry)
"""


class TelegramClient:
    parse_modes = {"html": "Html", "md": "MarkdownV2", "text": None}
    url = f"{settings.TELEGRAM_BASE_URL}/sendMessage"
    headers = {"Content-Type": "application/json"}

    def body(self, text, chat_id=settings.TELEGRAM_CHAT_ID, parse="text"):
        assert parse in self.parse_modes, "Unknown parse mode"
        body = dict(chat_id=chat_id, text=text, disable_notification=False)
        if parse_mode := self.parse_modes[parse]:
            body["parse_mode"] = parse_mode
        return body

    def send(self, text, chat_id=None, parse="text"):
        chat_id = chat_id or settings.TELEGRAM_CHAT_ID
        body = self.body(text, chat_id=chat_id, parse=parse)
        response = requests.post(self.url, json=body, headers=self.headers)

        if response.status_code >= 400:
            self.send_error(response, chat_id)
            return

        print("TelegramBot:", response.json())

    def send_error(self, response: requests.Response, chat_id=str):
        print(f"Telegram err: {response.content}")
        err = json.dumps(json.loads(response.content), indent=2)
        body = self.body(f"Telegram send error:\n{err}", chat_id=chat_id)
        requests.post(self.url, json=body, headers=self.headers)


class TelegramListener:
    def __init__(self):
        self.gcal = CalendarClient()
        self.client = TelegramClient()
        self.send = self.client.send
        self.updates_url = f"{settings.TELEGRAM_BASE_URL}/getUpdates?"

    def handle_add(self, payload, chat_id):
        try:
            date, name = re.match(r"(\d{4}-\d{2}-\d{2})\s(.*)", payload).groups()
            self.gcal.add_event(date, name)
            self.send(f"Success! I have added {date} for {name}", chat_id=chat_id)
        except Exception as e:
            print("ERROR", e)
            self.send("Wrong payload. Please send as 2022-01-01 Jeroen", chat_id=chat_id)

    def handle_update(self, update):
        message = update["message"]
        chat_id = message["chat"]["id"]

        text = message.get("text", "")
        entities = message.get("entities", [])
        if len(entities) == 0:
            return

        if entities[0]["type"] != "bot_command":
            return

        length = entities[0]["length"]
        cmd = text[:length]
        payload = text[length + 1 :]

        if cmd == "/help":
            self.send(HELP, chat_id=chat_id)
        elif cmd == "/ping":
            self.send("👋 I'm alive!", chat_id=chat_id)
        elif cmd == "/upcoming":
            events = [event.for_telegram for event in self.gcal.upcoming()]
            self.send("\n".join(events), chat_id=chat_id)
        elif cmd == "/add":
            self.handle_add(payload, chat_id=chat_id)
        else:
            self.send("I don't understand that", chat_id=chat_id)

    def handle_notify(self):
        for event in self.gcal.upcoming():
            if event.is_today:
                key = f"{event.state_key}-today"
                if key not in state.past:
                    self.send(f"It's {event.summary}'s bday today!")
                    state.past[key] = "1"
            if event.is_next_week:
                key = f"{event.state_key}-nextweek"
                if key not in state.past:
                    self.send(f"It's {event.summary}'s bday next week.")
                    state.past[key] = "1"

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
                if update.get("message"):
                    self.handle_update(update)
            except:
                traceback.print_exc()


async def main():
    telegram = TelegramListener()
    telegram.send("Server started")
    await asyncio.gather(telegram.listen())


if __name__ == "__main__":
    print("Let's go")
    asyncio.run(main())
