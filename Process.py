from threading import Thread
from time import sleep
from Com import Com


class Process(Thread):
    """
    A class to represent a process in a distributed system.

    Attributes:
        com (Com): The communication object for the process.
        nbProcess (int): The total number of processes.
        myId (int): The ID of the current process.
        alive (bool): A flag to indicate if the process is running.
    """

    def __init__(self, name, nbProcess):
        """
        Initialize a new process.

        Args:
            name (str): The name of the process.
            nbProcess (int): The total number of processes.
        """
        Thread.__init__(self)
        self.com = Com(nbProcess)
        self.nbProcess = nbProcess
        self.myId = self.com.get_my_id()
        self.setName(name)
        self.alive = True
        self.start()

    def run(self):
        """
        The main loop of the process. Executes the process logic.
        """
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
                    print(str(msg.get_sender()) + " a eu le jeton en premier")
                self.com.release_sc()

            if self.getName() == "P1":
                while not self.com.mailbox_is_empty():
                    msg = self.com.get_from_mailbox()
                    print(f"{self.getName()} received: {msg.get_message()} from {msg.get_sender()}")
                    self.com.receive_from_sync()
                self.com.synchronize()
                self.com.request_sc()
                if self.com.mailbox_is_empty():
                    print("Catched !")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    msg = self.com.get_from_mailbox()
                    print(str(msg.get_sender()) + " a eu le jeton en premier")
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
                    print(str(msg.get_sender()) + " a eu le jeton en premier")
                self.com.release_sc()

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        """
        Stop the process.
        """
        self.alive = False
        self.join()
