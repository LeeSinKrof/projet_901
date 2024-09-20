from threading import Thread
from time import sleep
from Com import Com


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
            sleep(1)

            if self.getName() == "P0":
                self.com.send_to("j'appelle 2 et je te recontacte après", 1)

                self.com.send_to_sync(
                    "J'ai laissé un message à 2, je le rappellerai après, on se sychronise tous et on attaque la partie ?",
                    2)
                self.com.receive_from_sync()

                self.com.send_to_sync("2 est OK pour jouer, on se synchronise et c'est parti!", 1)

                self.com.synchronize()

                self.com.request_sc()
                if self.com.mailbox_is_empty():
                    print("Catched !")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    msg = self.com.get_from_mailbox()
                    print(str(msg.getSender()) + " à eu le jeton en premier")
                self.com.release_sc()

            if self.getName() == "P1":
                if not self.com.mailbox_is_empty():
                    self.com.get_from_mailbox()
                    self.com.receive_from_sync()

                    self.com.synchronize()

                    self.com.request_sc()
                    if self.com.mailbox_is_empty():
                        print("Catched !")
                        self.com.broadcast("J'ai gagné !!!")
                    else:
                        msg = self.com.get_from_mailbox()
                        print(str(msg.getSender()) + " à eu le jeton en premier")
                    self.com.release_sc()

            if self.getName() == "P2":
                self.com.receive_from_sync()
                self.com.send_to_sync("OK", 0)

                self.com.synchronize()

                self.com.request_sc()
                if self.com.mailbox_is_empty():
                    print("Catched !")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    msg = self.com.get_from_mailbox()
                    print(str(msg.getSender()) + " à eu le jeton en premier")
                self.com.release_sc()

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
