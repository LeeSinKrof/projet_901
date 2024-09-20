from threading import Thread
from time import sleep
from Com import Com
import random

class Process(Thread):

    def __init__(self, name, nbProcess):
        Thread.__init__(self)

        self.com = Com(nbProcess)

        self.nbProcess = nbProcess
        self.myId = self.com.get_my_id()
        self.setName(name)

        self.alive = True
        self.start()

    def run(self):
        loop = 0

        while self.alive:
            print(self.getName() + " Loop: " + str(loop))

            action = random.choice(["send_message", "broadcast", "request_sc", "sync"])

            if action == "send_message":
                receiver = random.randint(0, self.nbProcess - 1)
                message = f"Message from {self.getName()} to Process {receiver}"
                self.com.send_to(message, receiver)

            elif action == "broadcast":
                message = f"Broadcast message from {self.getName()}"
                self.com.broadcast(message)

            elif action == "request_sc":
                print(self.getName() + " requesting critical section")
                self.com.request_sc()
                print(self.getName() + " entering critical section")
                sleep(2)
                print(self.getName() + " releasing critical section")
                self.com.release_sc()

            elif action == "sync":
                print(self.getName() + " attempting to synchronize with other processes")
                self.com.synchronize()

            sleep(random.uniform(0.5, 2))

            loop += 1

        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
