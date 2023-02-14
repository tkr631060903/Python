from threading import RLock
from time import sleep
import pyvisa
from ..common.common import Dev


class LCRX():
    """
    Arguments:
        rc {str} -- VISA资源列表
        instrument {str} -- 指定型号
    """

    def __init__(self, rc, instrument=None, sel=0):
        """
        Arguments:
            rc {str} -- VISA资源列表
            instrument {str} -- 指定型号
        """
        cfg = {
            "rc": rc,
            "instrument": instrument,
            "sel": sel,
            "key": [{
                "manufacturer": "Tonghui",
                "model": None
            }]
        }
        dev = Dev(cfg)
        # info = dev.get_info()
        rm = pyvisa.ResourceManager()
        print(dev.addr)
        self.heromix = rm.open_resource(dev.addr)
        # Set Global Timeout
        self.heromix.timeout = 5000
        # Clear the instrument bus
        self.heromix.clear()
        self.xlock = RLock()

    def close(self):
        self.heromix.close()

    def IDN(self):
        """获取示波器的身份标示IDN"""
        IDN = self.heromix.query("*IDN?")
        return IDN

    def CLS(self):
        """清除寄存器的值"""
        self.heromix.write('*CLS')

    def RST(self):
        """复位"""
        self.heromix.query('*RST')

    def get_measure_val(self, func, freq, val=1.0):
        self.heromix.write('FREQ {0}'.format(freq))
        self.heromix.write('VOLT {0}'.format(val))
        self.heromix.write('FUNC:IMP {0}'.format(func))
        # self.heromix.write('TRIG:SOUR BUS')
        # self.heromix.write('TRIG')
        sleep(0.5)
        result = self.heromix.query('FETC?')
        val1 = float(result.split(",")[0])
        val2 = float(result.split(",")[1])
        return val1, val2

    def correct_short(self, func):
        self.heromix.write('FUNC:IMP {0}'.format(func))
        self.heromix.write('CORR:SHOR:STAT {0}'.format("ON"))
        self.heromix.write('CORR:OPEN:STAT {0}'.format("OFF"))
        self.heromix.write('CORR:LOAD:STAT {0}'.format("OFF"))


if __name__ == "__main__":
    pass
