from pyeventbus3.pyeventbus3 import *
from time import sleep
from Message import *
from threading import Lock


class Com:
    nbProcessCreated = 0

    def __init__(self, nb_process):

        self.myId = Com.nbProcessCreated
        self.nbProcess = nb_process
        self.name = "P" + str(self.myId)
        Com.nbProcessCreated += 1

        PyBus.Instance().register(self, self)

        self.clock = 0
        self.state = State.NONE
        self.cpt_synchro = nb_process
        self.mailbox = []
        self.message_received = False
        self.lock = Lock()

    @staticmethod
    def get_nb_process():
        return Com.nbProcessCreated

    def get_my_id(self):
        return self.myId

    def get_name(self):
        return self.name

    def add_to_mailbox(self, message):
        with self.lock:
            self.mailbox.append(message)

    def get_from_mailbox(self):
        with self.lock:
            if self.mailbox:
                return self.mailbox.pop(0)
            return None

    def mailbox_is_empty(self):
        with self.lock:
            return len(self.mailbox) == 0

    def inc_clock(self):
        with self.lock:
            self.clock += 1

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def on_receive(self, event):
        if event.get_receiver() == self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            print(self.get_name() + ' received message: ' + str(event.get_message()) + " Clock: " + str(self.clock))

    def send_to(self, message, receiver):
        self.inc_clock()
        msg = MessageTo(self.myId, message, receiver, self.clock)
        PyBus.Instance().post(msg)
        print(self.get_name() + " sent: " + str(msg.get_message()) + " Clock: " + str(self.clock))

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def on_broadcast(self, event):
        if event.get_sender() != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            print(self.get_name() + ' received broadcast: ' + str(event.get_message()) + " Clock: " + str(self.clock))

    def broadcast(self, message):
        self.inc_clock()
        msg = BroadcastMessage(self.myId, message, self.clock)
        print(self.get_name() + " sent broadcast: " + str(msg.get_message()) + " Clock: " + str(self.clock))
        with self.lock:
            PyBus.Instance().post(msg)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TokenMessage)
    def on_token(self, event):
        if event.get_sender() == self.myId:
            if self.state == State.REQUEST:
                self.state = State.SC
                print(self.get_name() + " received token")
                while self.state == State.SC:
                    sleep(1)

            self.state = State.RELEASE
            self.send_token()

    def send_token(self):
        token = TokenMessage((self.myId + 1) % self.nbProcess)
        PyBus.Instance().post(token)

    def request_sc(self):
        self.state = State.REQUEST
        while self.state == State.REQUEST:
            sleep(1)

    def release_sc(self):
        self.state = State.RELEASE

    @subscribe(threadMode=Mode.PARALLEL, onEvent=SynchronizationMessage)
    def on_sync(self, event):
        if event.get_sender() != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.cpt_synchro -= 1

    def synchronize(self):
        self.inc_clock()
        PyBus.Instance().post(SynchronizationMessage(self.myId, self.clock))
        print(self.get_name() + " waiting for synchronization")
        while self.cpt_synchro > 1:
            print(self.get_name() + " is waiting for " + str(self.cpt_synchro) + " processes")
            sleep(1)
        print(self.get_name() + " is synchronized")
        self.cpt_synchro = self.nbProcess

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessageSync)
    def on_broadcast_sync(self, event):
        if event.get_sender() != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            self.message_received = True

    def broadcast_sync(self, message, sender):
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
        if event.get_sender() == self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            self.message_received = True

    def receive_from_sync(self):
        while not self.message_received:
            sleep(1)
        final_msg = self.get_from_mailbox()
        msg = MessageToSync("", final_msg.get_sender(), self.clock)
        PyBus.Instance().post(msg)
        self.message_received = False

    @subscribe(threadMode=Mode.PARALLEL, onEvent=ReceivedMessageSync)
    def receive_message_sync_reply(self, event):
        if event.get_receiver() == self.myId:
            with self.lock:
                self.clock = max(self.clock, event.get_stamp()) + 1
            self.add_to_mailbox(event)
            self.message_received = True

    def send_to_sync(self, message, receiver):
        self.inc_clock()
        msg = MessageToSync(message, receiver, self.clock)
        PyBus.Instance().post(msg)
        while not self.message_received:
            sleep(1)
        self.message_received = False
