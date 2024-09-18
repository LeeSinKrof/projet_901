from threading import Lock, Semaphore
from time import sleep

from Message import Message

class Com:
    def __init__(self):
        self.lamport_clock = 0
        self.clock_lock = Semaphore()

    def inc_clock(self):
        with self.clock_lock:
            self.lamport_clock += 1