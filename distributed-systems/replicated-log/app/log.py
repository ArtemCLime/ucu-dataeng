import uuid
import datetime
from logger import get_logger

logger = get_logger()


class MessageLog:
    def __init__(self):
        self.messages = []
        self.ids = set()

    def append(self, message):
        if message.message_id in self.ids:
            logger.warn("[WARNING] Message already in log")
            return
        self.ids.add(message.message_id)
        self.messages.append(message)

    def get_all_messages(self):
        sorted_messages = sorted(self.messages, key=lambda x: x.timestamp)
        return [message.message for message in sorted_messages]

    def clean(self):
        self.messages = []
        self.ids = set()


class Message:
    def __init__(self, message, message_id=None, timestamp=None):
        self.message = message
        if message_id is None:
            self.message_id = uuid.uuid4()
        else:
            self.message_id = message_id
        if timestamp is None:
            self.timestamp = datetime.datetime.now()
        else:
            self.timestamp = timestamp

    def to_json(self):
        return {
            "message": self.message,
            "message_id": self.message_id,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message
