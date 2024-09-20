from threading import Lock, Semaphore
from time import sleep

from Message import *

from pyeventbus3.pyeventbus3 import *

class Com(Thread):
    nbProcessCreated = 0
    def __init__(self, name, nbProcess, process):
        Thread.__init__(self)

        self.process = process
        self.nbProcess = nbProcess
        self.myId = Com.nbProcessCreated
        Com.nbProcessCreated += 1

        PyBus.Instance().register(self, self)

        self.clock = 0
        self.mailbox = []
        self.lock = Lock()
        self.message_received = False


    def inc_clock(self):
        with self.lock:
            self.clock += 1

    def getMyId(self):
        return self.myId

    def send_to(self, msg, to):
        self.inc_clock()
        message = MessageTo(self.myId, msg, to, self.clock)
        PyBus.Instance().post(message)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def on_receive(self, event):
        if event.receiver == self.getMyId():
            with self.lock:
                self.clock = max(self.clock, event.stamp)
                self.inc_clock()
                self.mailbox.append(event)
            print(f"{self.myId} received message: {event.message}")


    def broadcast(self, msg):
        self.inc_clock()
        message = BroadcastMessage(self.myId, msg, self.clock)
        PyBus.Instance().post(message)
        print(f"{self.myId} broadcasted message: {msg}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def on_broadcast(self, event):
        if event.sender != self.myId:
            with self.lock:
                self.clock = max(self.clock, event.clock)
                self.inc_clock()
                if event not in self.mailbox:
                    self.mailbox.append(event)
            print(f"{self.myId} received broadcast: {event.message}")


    @subscribe(threadMode=Mode.PARALLEL, onEvent=TokenMessage)
    def on_token(self, event):
        if event.receiver == self.myId and self.process.alive:
            if self.process.state == State.REQUEST:
                self.process.state = State.SC
                while self.process.state != State.RELEASE:
                    sleep(1)
                PyBus.Instance().post(TokenMessage((self.myId + 1) % self.nbProcess))
                self.process.state = State.NONE

    def request_sc(self):
        self.process.state = State.REQUEST
        while self.process.state != State.SC:
            sleep(1)

    def release_sc(self):
        self.process.state = State.RELEASE

    @subscribe(threadMode=Mode.PARALLEL, onEvent=SynchronizationMessage)
    def on_synchronize(self, event):
        if event.sender != self.myId:
            self.process.cpt_sync -= 1

    def synchronize(self):
        PyBus.Instance().post(SynchronizationMessage(self.myId, self.clock))
        while self.process.cpt_sync > 0:
            sleep(1)
        self.process.cpt_sync = self.nbProcess - 1

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessageSync)
    def on_broadcast_sync(self, event):
        if event.sender != self.myId:
            if event.clock > self.clock:
                self.clock = event.clock
            else:
                self.inc_clock()

            self.mailbox.append(event)
            self.message_received = True

    def broadcast_sync(self, sender, msg):
        if sender == self.myId:
            if msg is not None:
                self.inc_clock()
                message = BroadcastMessageSync(sender, msg, self.clock)
                PyBus.Instance().post(message)
            print(f"{self.myId} broadcasted message: {msg}")
            self.synchronize()
        else:
            while not self.message_received:
                sleep(1)
            print(f"{self.myId} received message: {msg}")
            self.synchronize()
            self.message_received = False

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageToSync)
    def on_receive_sync(self, event):
        if event.receiver == self.myId:
            if event.stamp > self.clock:
                self.clock = event.stamp
            else:
                self.inc_clock()
            self.mailbox.append(event)
            self.message_received = True

    def send_to_sync(self, msg, to):
        self.inc_clock()
        message = MessageToSync(self.myId, msg, to, self.clock)
        PyBus.Instance().post(message)
        print(f"{self.myId} sent message: {msg} to {to}")
        while not self.message_received:
            sleep(1)
        self.message_received = False

    def receive_from_sync(self, _from):
        print(f"{self.myId} is waiting for message from {_from}")
        while not self.message_received:
            sleep(1)  # Attendre la réception du message
        message = self.mailbox.get()
        print(f"{self.myId} received message from {_from}: {message}")
        self.message_received = False



    @subscribe(threadMode=Mode.PARALLEL, onEvent=ReceivedMessageSync)
    def on_received_sender_sync(self, event):
        if event.receiver == self.myId:
            print(f"{event.receiver} received message from {event.sender}")
            if event.stamp > self.clock:
                self.clock = event.stamp
            else:
                self.inc_clock()
            self.message_received = True













