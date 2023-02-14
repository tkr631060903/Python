import serial
import serial.tools.list_ports
from time import sleep
from ..devInfo.devInfo import devInfo


class CRAFT(object):
    """
    Arguments:
        addr {str} -- 通讯参数
    """

    def tryconnect(self, addr):
        if addr.find("COM") == 0:
            try_cnt = 0
            while self._ser is None and try_cnt < 3:
                try_cnt += 1
                try:
                    ser = serial.Serial(addr, 115200, timeout=1)
                    cmd = "$help#"
                    cmd = cmd.encode("ascii")
                    ser.write(cmd + b"\n")
                    sleep(0.1)
                    str_tmp = str(ser.read_all().decode("ascii"))
                    ser.close()
                    if str_tmp.find("help information") == 0:
                        print(addr)
                        self._ser = serial.Serial(addr, 115200, timeout=1)
                        if addr is not self.addr_cfg:
                            self.addrInfo.setAddr("craft", addr)
                        return
                except Exception:
                    try_cnt = 3

    def __init__(self, rc=None, instrument=None, sel=0):
        self.addrInfo = devInfo()
        self._ser = None
        self.addr_cfg = self.addrInfo.getAddr("craft")
        self.tryconnect(self.addr_cfg)
        for port in list(serial.tools.list_ports.comports()):
            if self._ser is None:
                self.tryconnect(port[0])
        # addrInfo.setAddr("signalgen", "")
        # print("try connect times:", try_cnt)

    def close(self):
        """关闭设备通讯
        """
        self._ser.close()

    def setChan(self, msk=[False] * 32):
        mask = 0
        for m in reversed(msk):
            if m:
                mask += 1
            mask *= 2
        mask //= 2
        cmd = "$CMFFFFFFFF#$SM{0}#".format(
            hex(mask).split("0x")[1].rjust(8, "0"))
        return self.exchange(cmd)

    def setOFF(self, msk=[True] * 32):
        mask = 0
        for m in msk:
            if m:
                mask += 1
            mask *= 2
        mask = str(mask, 16)
        return self.exchange("$CM{0}#".format(mask))

    def exchange(self, cmd):
        cmd = cmd.encode("ascii")
        self._ser.flushInput()
        self._ser.write(cmd + b"\n")
        ret = self._ser.readline()
        if ret == b"":
            return ""
            # raise TimeoutError()
        return ret[:-1].decode("ascii")  # Ditch the newline


if __name__ == '__main__':
    mycraft = CRAFT()
    # print(mycraft.setChan(1, "FFFFFFFF"))
    # print(mygen.IDN())
    # mygen.set_output(1, None, "ON")
    # mygen.set_output(2, None, "OFF")
    # # mygen.set_source_apply_sinusoid('1', '200.340', '5.2', '2')
    # # mygen.set_source_apply_triangle('2', "20000.89", '2.4', '1.3')

    # mygen.set_source_apply_square(1, 500*1000, 3, 1.5, 0)
    # mygen.set_source_apply_square(2, 500*1000, 3, 1.5, 0)
    # # mygen.set_output(1, "STAT", "ON")
    # # mygen.set_output(2, "STAT", "ON")
