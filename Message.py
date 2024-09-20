from abc import ABC
from enum import Enum


class Message(ABC):
    def __init__(self, sender, message, receiver, stamp):
        self.sender_id = sender
        self.message = message
        self.receiver = receiver
        self.stamp = stamp


class State(Enum):
    NONE = None
    REQUEST = "REQUEST"
    SC = "SC"
    RELEASE = "RELEASE"


class BroadcastMessage(Message):
    def __init__(self, sender, message, stamp):
        super().__init__(sender=sender, message=message, stamp=stamp)


class MessageTo(Message):
    def __init__(self, sender, message, receiver, stamp):
        super().__init__(sender, message, receiver, stamp)


class TokenMessage(Message):
    def __init__(self, sender):
        super().__init__(sender, message="Ceci est un TOKEN")


class SynchronizationMessage(Message):
    def __init__(self, sender, stamp):
        super().__init__(sender, stamp=stamp)


class BroadcastMessageSync(Message):
    def __init__(self, sender, message, stamp):
        super().__init__(sender, message, stamp=stamp)


class MessageToSync(Message):
    def __init__(self, sender, message, receiver, stamp):
        super().__init__(sender, message, receiver, stamp)


class ReceivedMessageSync(Message):
    def __init__(self, sender, receiver, stamp):
        super().__init__(sender, receiver=receiver, stamp=stamp)
