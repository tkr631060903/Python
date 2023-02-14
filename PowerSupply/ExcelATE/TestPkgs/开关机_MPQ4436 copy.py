# coding: utf-8
import sys
from corelib.autolib import ATS
from time import clock, sleep

if __name__ == "__main__":
    l_loadcurrent = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    while True:
        for i in range(len(l_loadcurrent)):
            print(l_loadcurrent[i])
            sleep(1)