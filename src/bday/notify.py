from bday.telegram import Telegram
from bday.gcal import CalendarClient


def handle_notify():
    client = Telegram()
    events = CalendarClient().upcoming()

    for event in events:
        if event.should_notify:
            client.send(event.notify_text)

    client.send("Done checking bdays!")


if __name__ == "__main__":
    print("Let's go notify")
    handle_notify()
