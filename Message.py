from abc import ABC
from enum import Enum

class Message(ABC):
    def __init__(self, sender, message, receiver):
        self.sender_id = sender
        self.message = message
        self.receiver = receiver
        self.clock = None


class sendMessageTo(Message):
    def __init__(self, sender, message, receiver):
        super().__init__(sender, message, receiver)

class broadcastMessage(Message):
    def __init__(self, sender, message):
        super().__init__(sender, message)

class tokenMessage(Message):
    def __init__(self, sender):
        super().__init__(sender, "Ceci est un Token")

class State(Enum):
    NONE = None
    REQUEST = "REQUEST"
    SC = "SC"
    RELEASE = "RELEASE"

class syncMessage(Message):
    def __init__(self, sender):
        super().__init__(sender)
