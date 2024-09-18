import threading

from pyeventbus3.pyeventbus3 import *
from Message import *

class Com:
    def __init__(self, clock):
        self.clock = 0
        self.message = None
        self.nbProcess = None
        self.myId = None
        self.mailbox = None

    def inc_clock(self):
        self.clock += 1

    def getMessage(self):
        return self.message


    def getClock(self):
        return self.clock

    def getNbProcess(self):
        return self.nbProcess

    def getMyId(self):
        return self.myId

    def getMailbox(self):
        return self.mailbox

    def sendTo(self, message, to):
        pass

    def sendToSync(self, message, to):
        pass

    def recevFromSync(self, message, fromId):
        pass

    def synchronize(self):
        pass

    def requestSC(self):
        pass

    def releaseSC(self):
        pass

    def broadcast(self, message):
        pass



