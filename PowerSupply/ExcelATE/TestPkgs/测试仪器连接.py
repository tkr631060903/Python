# coding: utf-8
import sys
from corelib.autolib import ATS

if __name__ == "__main__":
    use_devices = ['电子负载']
    ATS.connect_devices(use_devices)
