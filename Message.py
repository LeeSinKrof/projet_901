from abc import ABC
from enum import Enum


class Message(ABC):
    """
    Abstract base class for messages in the system.

    Attributes:
        sender : The sender of the message.
        message : The content of the message.
        receiver : The receiver of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, message, receiver, stamp):
        """
        Initialize a new message.

        Args:
            sender: The sender of the message.
            message: The content of the message.
            receiver: The receiver of the message.
            stamp: The stamp of the message.
        """
        self.sender = sender
        self.message = message
        self.receiver = receiver
        self.stamp = stamp

    def get_sender(self) -> str:
        """
        Get the sender of the message.

        Returns:
            str: The sender of the message.
        """
        return self.sender

    def get_message(self) -> any:
        """
        Get the content of the message.

        Returns:
            any: The content of the message.
        """
        return self.message

    def get_receiver(self) -> str:
        """
        Get the receiver of the message.

        Returns:
            str: The receiver of the message.
        """
        return self.receiver

    def get_stamp(self) -> int:
        """
        Get the stamp of the message.

        Returns:
            int: The stamp of the message.
        """
        return self.stamp


class State(Enum):
    """
    Enumeration for the state of a process.
    """
    NONE = None
    REQUEST = "REQUEST"
    SC = "SC"
    RELEASE = "RELEASE"


class BroadcastMessage(Message):
    """
    Class for broadcast messages.

    Attributes:
        sender : The sender of the message.
        message : The content of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, message, stamp):
        """
        Initialize a new broadcast message.

        Args:
            sender : The sender of the message.
            message : The content of the message.
            stamp : The stamp of the message.
        """
        super().__init__(sender=sender, message=message, receiver=None, stamp=stamp)

    def __str__(self) -> str:
        """
        String representation of the broadcast message.

        Returns:
            str: The string representation of the broadcast message.
        """
        return f"{self.sender} broadcasts: {self.message}"


class MessageTo(Message):
    """
    Class for messages sent to a specific receiver.

    Attributes:
        sender : The sender of the message.
        message : The content of the message.
        receiver : The receiver of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, message, receiver, stamp):
        """
        Initialize a new message to a specific receiver.

        Args:
            sender : The sender of the message.
            message : The content of the message.
            receiver : The receiver of the message.
            stamp : The stamp of the message.
        """
        super().__init__(sender=sender, message=message, receiver=receiver, stamp=stamp)

    def __str__(self) -> str:
        """
        String representation of the message to a specific receiver.

        Returns:
            str: The string representation of the message.
        """
        return f"{self.sender} sends to {self.receiver}: {self.message}"


class TokenMessage(Message):
    """
    Class for token messages.

    Attributes:
        sender : The sender of the message.
    """

    def __init__(self, sender):
        """
        Initialize a new token message.

        Args:
            sender : The sender of the message.
        """
        super().__init__(sender=sender, message="Ceci est un TOKEN", receiver=None, stamp=None)

    def __str__(self) -> str:
        """
        String representation of the token message.

        Returns:
            str: The string representation of the token message.
        """
        return f"Token from {self.sender}"


class SynchronizationMessage(Message):
    """
    Class for synchronization messages.

    Attributes:
        sender : The sender of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, stamp):
        """
        Initialize a new synchronization message.

        Args:
            sender : The sender of the message.
            stamp : The stamp of the message.
        """
        super().__init__(sender=sender, message=None, receiver=None, stamp=stamp)

    def __str__(self) -> str:
        """
        String representation of the synchronization message.

        Returns:
            str: The string representation of the synchronization message.
        """
        return f"{self.sender} synchronizes at {self.stamp}"


class BroadcastMessageSync(Message):
    """
    Class for synchronized broadcast messages.

    Attributes:
        sender : The sender of the message.
        message : The content of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, message, stamp):
        """
        Initialize a new synchronized broadcast message.

        Args:
            sender : The sender of the message.
            message : The content of the message.
            stamp : The stamp of the message.
        """
        super().__init__(sender=sender, message=message, receiver=None, stamp=stamp)

    def __str__(self) -> str:
        """
        String representation of the synchronized broadcast message.

        Returns:
            str: The string representation of the synchronized broadcast message.
        """
        return f"{self.sender} broadcasts synchronously: {self.message}"


class MessageToSync(Message):
    """
    Class for synchronized messages sent to a specific receiver.

    Attributes:
        sender : The sender of the message.
        message : The content of the message.
        receiver : The receiver of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, message, receiver):
        """
        Initialize a new synchronized message to a specific receiver.

        Args:
            sender : The sender of the message.
            message : The content of the message.
            receiver : The receiver of the message.
            stamp: The stamp of the message.
        """
        super().__init__(sender=sender, message=message, receiver=receiver, stamp=None)

    def __str__(self) -> str:
        """
        String representation of the synchronized message to a specific receiver.

        Returns:
            str: The string representation of the synchronized message.
        """
        return f"{self.sender} sends synchronously to {self.receiver}: {self.message}"


class ReceivedMessageSync(Message):
    """
    Class for synchronized message replies.

    Attributes:
        sender : The sender of the message.
        receiver : The receiver of the message.
        message : The content of the message.
        stamp : The stamp of the message.
    """

    def __init__(self, sender, receiver, message, stamp):
        """
        Initialize a new synchronized message reply.

        Args:
            sender: The sender of the message.
            receiver: The receiver of the message.
            message: The content of the message.
            stamp: The stamp of the message.
        """
        super().__init__(sender=sender, message=message, receiver=receiver, stamp=stamp)

    def __str__(self) -> str:
        """
        String representation of the synchronized message reply.

        Returns:
            str: The string representation of the synchronized message reply.
        """
        return f"{self.receiver} received from {self.sender}: {self.message}"
