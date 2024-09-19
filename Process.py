from threading import Thread
from time import sleep
from Com import Com

class Process(Thread):

    def __init__(self, name, nbProcess):
        Thread.__init__(self)

        self.com = Com()

        self.nbProcess = nbProcess
        self.myId = self.com.getMyId()
        self.setName(name)

        self.alive = True
        self.start()

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P0":
                self.com.sendTo("j'appelle 2 et je te recontacte après", 1)

                self.com.sendToSync("J'ai laissé un message à 2, je le rappellerai après, on se synchronise tous et on attaque la partie ?", 2)
                msg = self.com.recevFromSync(None, 2)

                self.com.sendToSync("2 est OK pour jouer, on se synchronise et c'est parti!", 1)

                self.com.synchronize()

                self.com.requestSC()
                if self.com.mailbox.empty():
                    print("Catched!")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    msg = self.com.mailbox.get()
                    print(str(msg.getSender()) + " a eu le jeton en premier")
                self.com.releaseSC()

            elif self.getName() == "P1":
                if not self.com.mailbox.empty():
                    self.com.mailbox.get()
                    self.com.recevFromSync(None, 0)

                    self.com.synchronize()

                    self.com.requestSC()
                    if self.com.mailbox.empty():
                        print("Catched!")
                        self.com.broadcast("J'ai gagné !!!")
                    else:
                        msg = self.com.mailbox.get()
                        print(str(msg.getSender()) + " a eu le jeton en premier")
                    self.com.releaseSC()

            elif self.getName() == "P2":
                self.com.recevFromSync(None, 0)
                self.com.sendToSync("OK", 0)

                self.com.synchronize()

                self.com.requestSC()
                if self.com.mailbox.empty():
                    print("Catched!")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    msg = self.com.mailbox.get()
                    print(str(msg.getSender()) + " a eu le jeton en premier")
                self.com.releaseSC()

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
