from abc import ABC
from enum import Enum


class Message(ABC):
    def __init__(self, sender, message, receiver, stamp):
        self.sender = sender
        self.message = message
        self.receiver = receiver
        self.stamp = stamp

    def get_sender(self):
        return self.sender

    def get_message(self):
        return self.message

    def get_receiver(self):
        return self.receiver

    def get_stamp(self):
        return self.stamp


class State(Enum):
    NONE = None
    REQUEST = "REQUEST"
    SC = "SC"
    RELEASE = "RELEASE"


class BroadcastMessage(Message):
    def __init__(self, sender, message, stamp):
        super().__init__(sender=sender, message=message, receiver=None, stamp=stamp)


class MessageTo(Message):
    def __init__(self, sender, message, receiver, stamp):
        super().__init__(sender=sender, message=message, receiver=receiver, stamp=stamp)


class TokenMessage(Message):
    def __init__(self, sender):
        super().__init__(sender=sender, message="Ceci est un TOKEN", receiver=None, stamp=None)


class SynchronizationMessage(Message):
    def __init__(self, sender, stamp):
        super().__init__(sender=sender, message=None, receiver=None, stamp=stamp)


class BroadcastMessageSync(Message):
    def __init__(self, sender, message, stamp):
        super().__init__(sender=sender, message=message, receiver=None, stamp=stamp)


class MessageToSync(Message):
    def __init__(self, message, receiver, stamp):
        super().__init__(sender=None, message=message, receiver=receiver, stamp=stamp)


class ReceivedMessageSync(Message):
    def __init__(self, sender, receiver, message, stamp):
        super().__init__(sender=sender, message=message, receiver=receiver, stamp=stamp)
