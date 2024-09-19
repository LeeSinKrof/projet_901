from time import sleep
from Process import Process

def launch(nbProcess, runningTime=5):
    processes = []

    for i in range(nbProcess):
        processes.append(Process("P"+str(i), nbProcess))

    sleep(runningTime)

    for p in processes:
        p.stop()


if __name__ == '__main__':

    #bus = EventBus.getInstance()

    launch(nbProcess=3, runningTime=10)

    #bus.stop()