from threading import RLock
import serial
import binascii

from ..devInfo.devInfo import devInfo


def cmd_pack(cmd, data=None, addr=0, cnt=25, start=0xAA):
    out = [start, addr, cmd]
    cmd_sum = start + addr + cmd
    for i in range(cnt - 3):
        tmp = 0
        if type(data) is int:
            if i == 0:
                tmp = data
        elif type(data) is list:
            if i < len(data):
                tmp = data[i]
        out.append(tmp)
        cmd_sum += tmp
    out.append(cmd_sum % 256)
    # print(str(out))
    return out


def float2list(data, cnt=4):
    out = []
    data *= 1000
    for i in range(cnt):
        out.append(int(data % 256))
        data /= 256
    return out


mode_dict = {"CURR": 0, "VOLT": 1, "POW": 2, "RES": 3}
dyn_mode_dict = {"CONT": 0, "PULS": 1, "TOGGL": 2}
onoff_dict = {"ON": 1, "OFF": 0, "1": 1, "0": 0, '': 1}


class EloadX(object):
    """电子负载驱动类
    Arguments:
        addr {str} -- 通讯参数
    """

    def tryconnect(self, addr):
        if addr.find("COM") == 0:
            try_cnt = 0
            while self._addr is None and try_cnt < 3:
                try_cnt += 1
                try:
                    with serial.Serial(addr, 9600, timeout=1) as ser:
                        ser.read_all()
                        ser.write(cmd_pack(0x20, 1))
                        info = binascii.b2a_hex(ser.read(26))
                    if info.find(b'aa001280') == 0:
                        print(addr)
                        self._addr = addr
                        if addr is not self.addr_cfg:
                            self.addrInfo.setAddr("eload", addr)
                        return
                except Exception:
                    try_cnt = 3

    def __init__(self, rc=None, instrument=None, sel=0):
        self.addrInfo = devInfo()
        self._addr = None
        self.addr_cfg = self.addrInfo.getAddr("eload")
        try:
            self.tryconnect(self.addr_cfg)
        except Exception:
            pass
        for port in list(serial.tools.list_ports.comports()):
            if self._addr is None:
                self.tryconnect(port[0])
        self.xlock = RLock()
        if self._addr is None:
            raise Exception("未检测到设备或设备占用!")
        self.set_system_remote()

    def close(self):
        """关闭设备通讯
        """
        pass

    def query(self, data):
        if self._addr is not None:
            self.xlock.acquire()
            with serial.Serial(self._addr, 9600, timeout=1) as ser:
                ser.read_all()
                ser.write(data)
                result = ser.read(26)
            self.xlock.release()
            return result

    def send(self, data):
        if self._addr is not None:
            self.xlock.acquire()
            with serial.Serial(self._addr, 9600, timeout=1) as ser:
                ser.write(data)
            self.xlock.release()

    def set_current(self, curr):
        """设置CC模式下的设定电流(A)
        Arguments:
            curr {num}
        """
        # Set / Read current value of CC mode
        self.send(cmd_pack(0x2A, float2list(curr * 10)))

    def set_resistance(self, res):
        """设置CR模式下的设定电阻(Ω)
        Arguments:
            curr {num}
        """
        # Set / Read current value of CC mode
        self.send(cmd_pack(0x30, float2list(res)))

    # 系统命令
    def set_system_remote(self):
        """设置系统为远程控制模式
        """
        self.send(cmd_pack(0x20, 1))

    # 输入设置命令
    def set_input(self, onoff=''):
        """Set the input on/off state
        Keyword Arguments:
            onoff {str} -- {0|1|OFF|ON} (default: {''})
        """
        if onoff in onoff_dict:
            # Set the input on/off state
            self.send(cmd_pack(0x21, onoff_dict[onoff]))
        else:
            raise Exception("type error!")

    def set_input_short(self, onoff=''):
        """设置短路功能的状态
        Keyword Arguments:
            onoff {num or str} -- [{0|1|OFF|ON} (default: {''})
        """
        if onoff in onoff_dict:
            self.send(cmd_pack(0x5D, onoff_dict[onoff]))
        else:
            raise Exception("type error!")

    def set_mode(self, func):
        """Set CC/CV/CW/CR operation mode of electronic load.
        Arguments:
            func {str} -- {CURR|VOLT|POW|RES|DYN|LED|IMP}
            #CURR: 定电流操作模式CC
            #VOLT：定电压操作模式CV
            #POW: 定功率操作模式CP
            #RES：定电阻操作模式CR
            #DYN：动态操作模式
            #LED：LED模式
            #IMP：定阻抗模式
        """
        if func in mode_dict:
            func = mode_dict[func]
            # Set CC/CV/CW/CR operation mode of electronic load.
            self.send(cmd_pack(0x28, func))
            # Work mode (0:FIXED,1:SHORT, 2:TRANSITION,3:LIST,4: BATTERY)
            self.send(cmd_pack(0x5D, 0))
        else:
            raise Exception("type error!")

    def set_dynamic(self, mode, high, ht, low, lt, slew=3):
        #     """设置动态模式下的高准位拉载电流持续时间(s)
        #     Arguments:
        #         mode {str} -- {CONT|PULS|TOGGL}
        #     """
        self.set_mode("CURR")
        data = float2list(high * 10)
        data += float2list(lt * 10, 2)
        data += float2list(low * 10)
        data += float2list(ht * 10, 2)
        if mode in dyn_mode_dict:
            data.append(dyn_mode_dict[mode])
        # Set CC mode transient current and timer parameter
        self.send(cmd_pack(0x32, data))
        # Work mode (0:FIXED,1:SHORT, 2:TRANSITION,3:LIST,4: BATTERY)
        self.send(cmd_pack(0x5D, 2))
        # Nomatter the current trigger souce it is,this command can provide a trigger signal
        self.send(cmd_pack(0x9D))

    #     return rstatus

    # 测量命令

    def get_measure_voltage(self):
        """查询电压平均值(V)
        Returns:
            {float} -- 电压平均值(V)
        """
        rev = self.query(cmd_pack(0x5F))[3:7]
        val = int.from_bytes(rev, 'little')
        val = val / 1000.0
        return val

    def get_measure_current(self):
        """查询电流平均值(A)
        Returns:
            {float} -- 电流平均值(A)
        """
        rev = self.query(cmd_pack(0x5F))[7:11]
        cur = int.from_bytes(rev, 'little')
        cur = cur / 10000.0
        return cur

    def get_measure_power(self):
        """查询功率平均值(W)
        Returns:
            {float} -- 功率平均值(W)
        """
        rev = self.query(cmd_pack(0x5F))[11:15]
        pw = int.from_bytes(rev, 'little')
        pw = pw / 1000.0
        return pw


def main():
    myEload = EloadX()
    print(myEload)
    # myEload.set_system_remote()
    myEload.set_input("ON")

    myEload.set_mode('RES')
    myEload.set_resistance(5.32)

    myEload.set_mode('CURR')
    myEload.set_current(1.097)

    # myEload.set_dynamic("CONT", 2.2, 0.001, 0.1, 0.0001)
    # myEload.set_mode('CURR')
    # print(myEload.get_current())
    # print(myEload._ser.query('CURR?'))
    # myEload.set_mode('VOLT')
    # print(myEload._ser.query('VOLT?'))


if __name__ == "__main__":
    main()
