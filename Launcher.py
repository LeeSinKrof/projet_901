from time import sleep
from Process import Process


def launch(nbProcess, runningTime):
    """
    Launches a specified number of processes and runs them for a given amount of time.

    Args:
        nbProcess (int): The number of processes to launch.
        runningTime (int): The time in seconds to run the processes.
    """
    processes = []

    for i in range(nbProcess):
        processes.append(Process("P" + str(i), nbProcess))

    sleep(runningTime)

    for p in processes:
        p.stop()


if __name__ == '__main__':
    # Launch 3 processes and run them for 10 seconds
    launch(nbProcess=3, runningTime=10)
