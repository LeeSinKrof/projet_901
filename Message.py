from abc import ABC

class Message(ABC):
    def __init__(self, sender, message, receiver, stamp):
        self.sender_id = sender
        self.message = message
        self.receiver = receiver
        self.stamp = stamp

class sendMessageTo(Message):
    def __init__(self, sender, message, receiver, stamp):
        super().__init__(sender, message, receiver, stamp)

class broadcastMessage(Message):
    def __init__(self, sender, message, stamp):
        super().__init__(sender, message, stamp)
