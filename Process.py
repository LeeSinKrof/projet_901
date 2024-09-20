from threading import Thread
from time import sleep
from Com import Com

class Process(Thread):

    def __init__(self, name, nbProcess):
        Thread.__init__(self)

        self.com = Com(name, nbProcess, self)

        self.nbProcess = nbProcess
        self.myId = self.com.getMyId()
        self.setName(name)
        self.state = None
        self.cpt_sync = 0

        self.alive = True
        self.start()

    def run(self):
        loop = 0
        while self.alive:
            print(f"{self.getName()} Loop: {loop}, Lamport Clock: {self.com.clock}")
            sleep(1)

            if self.getName() == "P0":
                print(f"{self.getName()} Envoi de message à P1")
                self.com.send_to("Message de P0 à P1", 1)
                print(f"{self.getName()} Synchronisation avec P2")
                self.com.send_to_sync("P0 se synchronise avec P2", 2)
                self.com.synchronize()

                self.com.request_sc()
                with self.com.lock:
                    if len(self.com.mailbox) == 0:
                        print(f"{self.getName()} a gagné la section critique!")
                        self.com.broadcast("J'ai gagné!!!")
                    else:
                        msg = self.com.mailbox.pop(0)
                        print(f"{msg.sender_id} a eu le jeton en premier")
                self.com.release_sc()

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
