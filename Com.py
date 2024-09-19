from threading import Lock, Semaphore
from time import sleep

from Message import *

from pyeventbus3.pyeventbus3 import *

class Com(Thread):
    def __init__(self, process, clock):
        Thread.__init__(self)
        self.clock = clock
        self.process = process
        self.myId = process.myId
        self.mailbox = []
        self.sem = Semaphore()

    def inc_clock(self):
        self.sem.acquire()
        self.clock += 1
        self.sem.release()


    def add_message_in_mailbox(self, message):
        self.mailbox.append(message)

    def getMyId(self):
        return self.myId

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def on_receive(self, event):
        if event.receiver == self.getMyId():
            if event.stamp > self.clock:
                self.clock = event.stamp
            else:
                self.inc_clock()
            self.mailbox.append(event)
            print(f"{event.receiver} received message from {event.sender}: {event.message}")

    def send_to(self, msg, to):
        self.inc_clock()
        message = MessageTo(self.myId, msg, to, self.clock)
        PyBus.Instance().post(message)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def on_broadcast(self, event):
        if event.sender != self.myId:
            if event.clock > self.clock:
                self.clock = event.clock
            else:
                self.inc_clock()
            if event not in self.mailbox:
                self.mailbox.append(event)
            print(f"{event.sender} received broadcasted message: {event.message}")

    def broadcast(self, msg):
        self.inc_clock()
        message = BroadcastMessage(self.myId, msg, self.clock)
        PyBus.Instance().post(message)
        print(f"{self.myId} broadcasted message: {msg}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TokenMessage)
    def on_token(self, event):
        if event.receiver == self.myId and self.process.alive:
            if self.process.state == State.REQUEST:
                self.process.state = State.SC
                print(f"{self.myId} has the token")
                






