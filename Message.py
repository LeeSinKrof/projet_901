from abc import ABC

class Message(ABC):
    def __init__(self, sender, message, receiver, stamp):
        self.sender_id = sender
        self.message = message
        self.receiver = receiver
        self.stamp = stamp

class sendTo(Message):
    def __init__(self, sender, message, receiver, stamp):
        super().__init__(sender, message, receiver, stamp)

    def send_message(self):
        print(f"Sending message '{self.message}' to {self.receiver}")

class broadcast(Message):
    def __init__(self, sender, message, stamp):
        super().__init__(sender, message, stamp)

    def send_message(self):
        print(f"Broadcasting message '{self.message}' to all")