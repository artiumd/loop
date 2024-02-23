import os
from src.loop import loop_over
import time


def show_pid(i):
    time.sleep(0.1)
    print(f'{i} on process {os.getpid()}')


if __name__ == '__main__':
    loop_over(range(100)).map(show_pid).concurrently('processes').exhaust()
