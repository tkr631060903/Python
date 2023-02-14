from threading import RLock
import pyvisa
from ..common.common import Dev


class DMMX():
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
                "manufacturer": "KEYSIGHT",
                "model": ["344"]
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
        """获取万用表的身份标示IDN"""
        IDN = self.heromix.query("*IDN?")
        return IDN

    def CLS(self):
        """清除寄存器的值"""
        self.heromix.write('*CLS')

    def RST(self):
        """复位"""
        self.heromix.query('*RST')

    def fetc(self):
        self.heromix.write('INIT')
        res = float(self.heromix.query('FETC?'))
        return res

    def conf(self, cfg):
        if self.heromix.query('CONF?').split(' ')[0].split('"')[1] != cfg:
            self.heromix.write('CONF:{0}'.format(cfg))

    def get_dc_val(self):
        self.conf('VOLT')
        val = float(self.fetc())
        return val

    def get_ac_val(self):
        self.conf('VOLT:AC')
        val = float(self.fetc())
        return val

    def get_dc_curr(self):
        self.conf('CURR')
        curr = float(self.fetc())
        return curr

    def get_ac_curr(self):
        self.conf('CURR:AC')
        curr = float(self.fetc())
        return curr

    def get_freq(self):
        self.conf('VOLT:AC')
        self.conf('FREQ')
        curr = float(self.fetc())
        return curr

    def get_res(self):
        self.conf('RES')
        res = float(self.fetc())
        return res


if __name__ == "__main__":
    pass
