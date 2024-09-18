from threading import Lock, Semaphore
from time import sleep

from Message import *

from pyeventbus3.pyeventbus3 import *

class Com:
    nbProcessCreated = 0
    def __init__(self, nbProcess, clock):
        self.clock = clock
        self.nbProcess = nbProcess
        self.myId = Com.nbProcessCreated
        Com.nbProcessCreated += 1
        self.mailbox = []
        self.sem = Semaphore()

    def inc_clock(self):
        with self.clock:
            self.sem.acquire()
            self.clock += 1
            self.sem.release()

    def getNbProcess(self):
        return self.nbProcess

    def getMyId(self):
        return self.myId

    @subscribe(threadMode=Mode.PARALLEL, onEvent=sendMessageTo)
    def onReceive(self, event):
        if event.receiver == self.getMyId():
            if event.stamp > self.clock:
                self.clock = event.stamp
            else:
                self.inc_clock()
            self.mailbox.append(event)
            print(f"{event.receiver} received message from {event.sender}: {event.message}")

    def sendTo(self, msg, to):
        self.inc_clock()
        message = sendMessageTo(self.myId, msg, to, self.clock)
        PyBus.Instance().post(message)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=broadcastMessage)
    def onBroadcast(self, event):
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
        message = broadcastMessage(self.myId, msg, self.clock)
        PyBus.Instance().post(message)