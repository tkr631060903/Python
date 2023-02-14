"""Cyclone control"""
from ctypes import (CDLL, POINTER, Structure, c_byte, c_char, c_char_p, c_int,
                    c_int16, c_int32, c_ubyte, c_uint, c_uint16, c_uint32,
                    c_void_p, cdll, windll)
from threading import RLock

import pyvisa


class CycloneControlX(object):
    """    
    """
    hadnle = 0

    def __init__(self, devType=0, devInd=0):
        from os import path
        thisfiledir = path.dirname(path.abspath(__file__))
        self.xlock = RLock()
        dllpath = path.join(thisfiledir, '_cdll', 'CycloneControlSDK.dll')
        print(dllpath)
        self.rm = cdll.LoadLibrary(dllpath)
        print(self.rm)

    def program(self):
        """烧写程序       
        """
        self.xlock.acquire()
        self.handle = self.rm.connectToCyclone(c_char_p(b'USB1'))
        if self.handle > 0:
            self.rm.startImageExecution(self.handle, 1)
            ret = 0
        else:
            self.rm.disconnectFromAllCyclones()
            ret = -1
        self.xlock.release()
        return ret

    def getProgram(self):
        """烧写程序       
        """
        self.xlock.acquire()
        self.rm.getDescriptionOfErrorCode.restype = c_char_p
        if self.handle > 0:
            while self.rm.checkCycloneExecutionStatus(self.handle) != 0:
                pass
            if self.rm.getNumberOfErrors(self.handle) != 0:
                ret = str(self.rm.getDescriptionOfErrorCode(
                    self.handle, self.rm.getErrorCode(self.handle, 1)),
                          encoding="utf-8")
            else:
                ret = "cyclone programmer program success!"
        self.rm.disconnectFromAllCyclones()
        self.xlock.release()
        return ret


if __name__ == "__main__":
    from time import sleep
    myCyclone = CycloneControlX()
    print(myCyclone.program())
    # sleep(2)