from abc import ABC
from enum import Enum

class Message(ABC):
    def __init__(self, sender=None, message=None, receiver=None, stamp=None):
        self.sender_id = sender
        self.message = message
        self.receiver = receiver
        self.stamp = stamp


class BroadcastMessage(Message):
    def __init__(self, sender, message, stamp=None):
        super().__init__(sender=sender, message=message, stamp=stamp)


class MessageTo(Message):
    def __init__(self, sender, message, receiver, stamp=None):
        super().__init__(sender=sender, message=message, receiver=receiver, stamp=stamp)


class TokenMessage(Message):
    def __init__(self, sender=None, receiver=None, stamp=None):
        super().__init__(sender=sender, receiver=receiver, message="Ceci est un TOKEN", stamp=stamp)
        self.nb_sync = 0


class State(Enum):
    NONE = None
    REQUEST = "REQUEST"
    SC = "SC"
    RELEASE = "RELEASE"


class SyncMessage(Message):
    def __init__(self, sender, stamp=None):
        super().__init__(sender=sender, message="SYNC", stamp=stamp)
