import requests
import json
import re

from bday import settings


class SkipTelegramMessage(Exception):
    pass


class InvalidBotCommand(Exception):
    pass


class TelegramMessage:
    def __init__(self, update: dict):
        try:
            self.message = update["message"]
            self.chat_id = self.message["chat"]["id"]
            self.text = self.message["text"]
            self.entities = self.message["entities"]

            assert self.entities[0]["type"] == "bot_command"
        except (KeyError, AssertionError):
            raise SkipTelegramMessage


class TelegramBotMessage(TelegramMessage):
    command_pattern = r"/(?P<command>\w+)(@bdaylertbot)? ?(?P<args>.*)?"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            text_match = re.match(self.command_pattern, self.text)
            assert text_match
            self.command = text_match.group("command")
            self.args = text_match.group("args")
        except AssertionError:
            raise InvalidBotCommand


class Telegram:
    parse_modes = {"html": "Html", "md": "MarkdownV2", "text": None}
    url = f"{settings.TELEGRAM_BASE_URL}/sendMessage"
    headers = {"Content-Type": "application/json"}

    def __init__(self, chat_id=None):
        self.default_chat_id = chat_id or settings.TELEGRAM_CHAT_ID

    def body(self, text, chat_id, parse="text"):
        assert parse in self.parse_modes, "Unknown parse mode"
        body = dict(chat_id=chat_id, text=text, disable_notification=False)
        if parse_mode := self.parse_modes[parse]:
            body["parse_mode"] = parse_mode
        return body

    def send(self, text, chat_id=None, parse="text"):
        chat_id = chat_id or self.default_chat_id
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
