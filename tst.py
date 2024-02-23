from os import getpid
from src.loop import loop_over


def show_pid(i):
    print(f'{i} on process {getpid()}')

    
loop_over(range(10)).map(show_pid).concurrently('processes').exhaust()
