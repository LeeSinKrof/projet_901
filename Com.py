from pyeventbus3.pyeventbus3 import *
from time import sleep
from Message import *
from threading import Lock


class IDManager:
    """
    A class to manage the IDs of the processes.

    Attributes:
        current_id (int): The current ID to assign to a process.
    """
    current_id = 0

    @staticmethod
    def get_new_id():
        new_id = IDManager.current_id
        IDManager.current_id += 1
        return new_id


class Com:
    """
    A class to represent a communication process in a distributed system.
    """

    def __init__(self, nb_process):
        """
        Initialize a new communication process.

        Args:
            nb_process (int): The total number of processes.
        """
        self.myId = IDManager.get_new_id()
        self.nbProcess = nb_process
        self.name = f"P{self.myId}"

        PyBus.Instance().register(self, self)

        self.clock = 0
        self.state = State.NONE
        self.cpt_synchro = nb_process
        self.mailbox = []
        self.message_received = False
        self.lock = Lock()
        self.alive = True

        if self.get_my_id() == self.nbProcess - 1:
            self.send_token()

    @staticmethod
    def get_nb_process():
        """
        Get the number of processes created.

        Returns:
            int: The number of processes created.
        """
        return IDManager.current_id

    def get_my_id(self):
        """
        Get the ID of the current process.

        Returns:
            int: The ID of the current process.
        """
        return self.myId

    def get_name(self):
        """
        Get the name of the current process.

        Returns:
            str: The name of the current process.
        """
        return self.name

    def add_to_mailbox(self, message):
        """
        Add a message to the mailbox.

        Args:
            message (Message): The message to add.
        """
        with self.lock:
            self.mailbox.append(message)
            print(f"{self.get_name()} added message to mailbox: {message.get_message()}")

    def get_from_mailbox(self):
        """
        Get a message from the mailbox.

        Returns:
            Message: The message from the mailbox.
        """
        with self.lock:
            return self.mailbox.pop(0)

    def mailbox_is_empty(self):
        """
        Check if the mailbox is empty.

        Returns:
            bool: True if the mailbox is empty, False otherwise.
        """
        with self.lock:
            return len(self.mailbox) == 0

    def inc_clock(self):
        """
        Increment the logical clock of the process.
        """
        with self.lock:
            self.clock += 1

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def on_broadcast(self, event):
        """
        Handle the reception of a broadcast message.

        Args:
            event (BroadcastMessage): The event containing the broadcast message.
        """
        if event.get_sender() != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            print(f"{self.get_name()} received broadcast: {event.get_message()} Clock: {self.clock}")

    def broadcast(self, message):
        """
        Broadcast a message to all processes.

        Args:
            message (str): The message to broadcast.
        """
        self.inc_clock()
        msg = BroadcastMessage(self.myId, message, self.clock)
        print(f"{self.get_name()} sent broadcast: {msg.get_message()} Clock: {self.clock}")
        with self.lock:
            PyBus.Instance().post(msg)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def on_receive(self, event):
        """
        Handle the reception of a message.

        Args:
            event (MessageTo): The event containing the message.
        """
        if event.get_receiver() == self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            print(f"{self.get_name()} received message: {event.get_message()} Clock: {self.clock}")

    def send_to(self, message, receiver):
        """
        Send a message to another process.

        Args:
            message (str): The message to send.
            receiver (int): The ID of the receiver process.
        """
        self.inc_clock()
        msg = MessageTo(self.myId, message, receiver, self.clock)
        PyBus.Instance().post(msg)
        print(f"{self.get_name()} sent: {msg.get_message()} Clock: {self.clock}")

    def request_sc(self):
        """
        Request to enter the critical section.
        """
        self.state = State.REQUEST
        while self.state == State.REQUEST:
            sleep(1)

    def release_sc(self):
        """
        Release the critical section.
        """
        self.state = State.RELEASE

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TokenMessage)
    def on_token(self, event):
        """
        Handle the reception of a token message.

        Args:
            event (TokenMessage): The event containing the token message.
        """
        if event.get_sender() == self.myId and self.state == State.REQUEST:
            self.state = State.SC
            print(f"{self.get_name()} received token")
            while self.state == State.SC:
                sleep(1)
            self.state = State.RELEASE
            self.send_token()

    def send_token(self):
        """
        Send a token to the next process.
        """
        token = TokenMessage((self.myId + 1) % self.nbProcess)
        PyBus.Instance().post(token)

    def synchronize(self):
        """
        Synchronize the process with other processes.
        """
        self.inc_clock()
        PyBus.Instance().post(SynchronizationMessage(self.myId, self.clock))
        print(f"{self.get_name()} waiting for synchronization")
        while self.cpt_synchro > 0:
            print(f"{self.get_name()} is waiting for {self.cpt_synchro} processes")
            sleep(0.1)
            if not self.alive:
                return
        print(f"{self.get_name()} is synchronized with all processes.")
        self.cpt_synchro = self.nbProcess


    @subscribe(threadMode=Mode.PARALLEL, onEvent=SynchronizationMessage)
    def on_sync(self, event):
        """
        Handle the reception of a synchronization message.

        Args:
            event (SynchronizationMessage): The event containing the synchronization message.
        """
        if event.get_sender() != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.cpt_synchro -= 1
            print(f"{self.get_name()} received synchronization from {event.get_sender()}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessageSync)
    def on_broadcast_sync(self, event):
        """
        Handle the reception of a synchronized broadcast message.

        Args:
            event (BroadcastMessageSync): The event containing the synchronized broadcast message.
        """
        if event.get_sender() != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            self.message_received = True

    def broadcast_sync(self, message, sender):
        """
        Broadcast a synchronized message.

        Args:
            message (str): The message to broadcast.
            sender (int): The ID of the sender process.
        """
        if self.myId == sender:
            self.inc_clock()
            msg = BroadcastMessageSync(self.myId, message, self.clock)
            PyBus.Instance().post(msg)
            self.synchronize()
        else:
            while not self.message_received:
                sleep(1)
            self.synchronize()
            self.message_received = False

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageToSync)
    def receive_message_sync(self, event):
        """
        Handle the reception of a synchronized message.

        Args:
            event (MessageToSync): The event containing the synchronized message.
        """
        if event.get_sender() == self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            self.message_received = True

    def receive_from_sync(self):
        """
        Receive a synchronized message from the mailbox.
        """
        while not self.message_received:
            sleep(0.1)
        final_msg = self.get_from_mailbox()
        msg = MessageToSync("", final_msg.get_sender(), self.clock)
        PyBus.Instance().post(msg)
        self.message_received = False

    @subscribe(threadMode=Mode.PARALLEL, onEvent=ReceivedMessageSync)
    def receive_message_sync_reply(self, event):
        """
        Handle the reception of a synchronized message reply.

        Args:
            event (ReceivedMessageSync): The event containing the synchronized message reply.
        """
        if event.get_receiver() == self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            self.message_received = True

    def send_to_sync(self, message, receiver):
        """
        Send a synchronized message to another process.

        Args:
            message (str): The message to send.
            receiver (int): The ID of the receiver process.
        """
        self.inc_clock()
        msg = MessageToSync(message, receiver, self.clock)
        PyBus.Instance().post(msg)
        while not self.message_received:
            sleep(0.1)
        self.message_received = False
