import sys
import os
sys.path.append(os.path.realpath("."))
from threading import RLock
import pyvisa
from TestPkgs.devLibs.common.common import Dev


class DCPowerX(object):
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
                "manufacturer": "ITECH",
                "model": ["IT6"]
            }]
        }
        dev = Dev(cfg)
        # info = dev.get_info()
        rm = pyvisa.ResourceManager()
        print(dev.addr)
        self.heromix = rm.open_resource(dev.addr)
        # Set Global Timeout
        self.heromix.timeout = 2000
        # Clear the instrument bus
        # self.heromix.clear()
        self.heromix.write('*CLS')
        self.heromix.write('SYST:REM')
        self.xlock = RLock()

    def close(self):
        """关闭设备通讯
        """
        self.heromix.close()

    # IEEE-488命令
    def IDN(self):
        """查询设备的身份信息
        Returns:
            {str} -- [description]
        """
        self.xlock.acquire()
        info = self.heromix.query('*IDN?')
        self.xlock.release()
        return info

    def RST(self):
        """恢复设备到工厂状态
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('*RST')
        self.xlock.release()
        return rstatus

    def CLS(self):
        """清除寄存器的值"""
        self.xlock.acquire()
        rstatus = self.heromix.write('*CLS')
        self.xlock.release()
        return rstatus

    # 系统命令
    def set_system_remote(self):
        """设置系统为远程控制模式
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SYST:REM')
        self.xlock.release()
        return rstatus

    # 输出命令

    def output(self, onoff):
        """打开或关闭电源输出
        Arguments:
            onoff {num or str} -- {0|1|OFF|ON}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('OUTP {0}'.format(onoff))
        self.xlock.release()
        return rstatus

    def output_timer(self, onoff):
        """控制电源输出定时器的状态
        Arguments:
            onoff {num or str} -- {0|1|OFF|ON}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('OUTP:TIM {0}'.format(onoff))
        self.xlock.release()
        return rstatus

    def output_timer_data(self, onoff):
        """设定电源输出定时器的时间
        Arguments:
            onoff {num or str} -- {0|1|OFF|ON}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('OUTP:TIM:DATA {0}'.format(onoff))
        self.xlock.release()
        return rstatus

    # 电流控制命令

    def set_current(self, curr):
        """设定电源输出电流(A)
        Arguments:
            curr {num or str} -- {<电流值>|MIN|MAX|UP|DOWN|DEF}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('CURR {0}'.format(curr))
        self.xlock.release()
        return rstatus

    def set_current_step(self, step):
        """设定电源输出电流步进值(A)
        Arguments:
            step {num} -- {MIN~MAX}例如 0.01 单位A
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('CURR:STEP {0}'.format(step))
        self.xlock.release()
        return rstatus

    def set_current_trig(self, curr):
        """设定一个等待触发的电流值(A)
        Arguments:
            curr {num} -- {MIN~MAX}例如 10 单位A
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('CURR:TRIG {0}'.format(curr))
        self.xlock.release()
        return rstatus

    def set_current_protection(self, curr):
        """设定过电流保护值(A)
        Arguments:
            curr {num} -- {MIN~MAX}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('CURR:PROT {0}'.format(curr))
        self.xlock.release()
        return rstatus

    def set_current_protection_state(self, onoff):
        """打开或关闭OCP功能，即设定过流保护状态
        Arguments:
            onoff {num or str} -- {0|1|ON|OFF}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('CURR:PROT:STAT {0}'.format(onoff))
        self.xlock.release()
        return rstatus

    def set_voltage(self, volt):
        """设定电源输出电压(V)
        Arguments:
            volt {num or str} -- 电压值(V)
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('VOLT {0}'.format(volt))
        self.xlock.release()
        return rstatus

    def set_voltage_step(self, step):
        """设定电源输出电压步进值(V)
        Arguments:
            step {num} -- {MIN~MAX}例如 0.01 单位V
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('VOLT:STEP {0}'.format(step))
        self.xlock.release()
        return rstatus

    def set_voltage_trig(self, volt):
        """设定一个等待触发的电压值(V)
        Arguments:
            step {num} -- {MIN~MAX}例如 10 单位V
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('VOLT:TRIG {0}'.format(volt))
        self.xlock.release()
        return rstatus

    def set_voltage_protection(self, volt):
        """设定过电压保护值(V)
        Arguments:
            volt {num} -- {MIN~MAX}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('VOLT:PROT {0}'.format(volt))
        self.xlock.release()
        return rstatus

    def set_voltage_protection_state(self, onoff):
        """打开或关闭OCP功能，即设定过压保护状态
        Arguments:
            onoff {num or str} -- {0|1|ON|OFF}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('VOLT:PROT:STAT {0}'.format(onoff))
        self.xlock.release()
        return rstatus

    def set_voltage_limit(self, volt):
        """设定输出电压范围的上限电压值(V)
        Arguments:
            volt {num} -- {MIN~MAX}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('VOLT:LIMIT {0}'.format(volt))
        self.xlock.release()
        return rstatus

    # 电池控制命令

    def set_batt_current(self, curr):
        """设定电池充电或放电电流(A)
        Arguments:
            curr {num or str} -- {<电流值>|MIN|MAX|UP|DOWN|DEF}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('BATT:CURR {0}'.format(curr))
        self.xlock.release()
        return rstatus

    def set_batt_voltage(self, volt):
        """设定电池充电或放电电压(V)
        Arguments:
            volt {num or str} -- 电压值(V)
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('BATT:VOLT {0}'.format(volt))
        self.xlock.release()
        return rstatus

    def set_batt_mode(self, mode):
        """设定电池充电或放电电压(V)
        Arguments:
            mode {str} -- {CHARge|DISCharge|SIMulator}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('BATT:MODE {0}'.format(mode))
        self.xlock.release()
        return rstatus

    def set_batt_status(self, status):
        """设定电池充电或放电电压(V)
        Arguments:
            status {str} -- {STARt|STOP}
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('BATT:{0}'.format(status))
        self.xlock.release()
        return rstatus

    # 测量命令

    def get_measure_current(self):
        """检测并返回当前的电流值(A)
        Returns:
            {float} -- [description]
        """
        self.xlock.acquire()
        val = self.heromix.query('MEAS:CURR?')
        self.xlock.release()
        return float(val)

    def get_fetch_current(self):
        """从缓存区读取其中最近的电流值(A)
        Returns:
            {float} -- [description]
        """
        self.xlock.acquire()
        val = self.heromix.query('FETC:CURR?')
        self.xlock.release()
        return float(val)

    def get_measure_voltage(self):
        """检测并返回当前的电压值(V)
        Returns:
            {float} -- [description]
        """
        self.xlock.acquire()
        val = self.heromix.query('MEAS:VOLT?')
        self.xlock.release()
        return float(val)

    def get_fetch_voltage(self):
        """从缓存区读取其中最近的电压值(V)
        Returns:
            {float} -- [description]
        """
        self.xlock.acquire()
        val = self.heromix.query('FETC:VOLT?')
        self.xlock.release()
        return float(val)

    def get_measure_power(self):
        """检测并返回当前的功率值(W)
        Returns:
            {float} -- [description]
        """
        self.xlock.acquire()
        val = self.heromix.query('MEAS:POW?')
        self.xlock.release()
        return float(val)

    def get_fetch_power(self):
        """从缓存区读取其中最近的功率值(W)
        Returns:
            {float} -- [description]
        """
        self.xlock.acquire()
        val = self.heromix.query('FETC:POW?')
        self.xlock.release()
        return float(val)

    def set_instchnl_select(self, ch):
        """选择通道
        Arguments:
            ch {[type]} -- {FIR|SECO|THI}
        """
        self.xlock.acquire()
        self.heromix.write('INST:SEL {0}'.format(ch))
        self.xlock.release()

    def set_list(self, group):
        self.xlock.acquire()
        self.heromix.write('LIST OFF')
        self.heromix.write('LIST:GRO {0}'.format(group["index"]))
        self.heromix.write('LIST:PER {0}'.format(group["repeat"]))
        cnt = 0
        for point in group["points"]:
            self.heromix.write('LIST:POIN {0}'.format(cnt))
            self.heromix.write('LIST:PAR {0}'.format(point))
            cnt += 1
        self.heromix.write('LIST:TOT {0}'.format(cnt))
        self.heromix.write('LIST:SAVE')
        self.heromix.write('TRIG:SOUR BUS')
        self.xlock.release()

    def set_list_run(self, sel):
        self.xlock.acquire()
        self.heromix.write('LIST ON')
        self.heromix.write('LIST:GRO:CLE:SEL')
        for i in sel:
            self.heromix.write('LIST:GRO:SEL {0}'.format(i))
        self.heromix.write('*TRG')
        self.xlock.release()


def main():
    # myDCPower = DCPowerX('ASRL4::INSTR')
    myDCPower = DCPowerX()
    print(myDCPower.IDN())
    # print(myDCPower.set_system_remote())
    # print(myDCPower.output('ON'))
    # sleep(1)
    # print('设置电压', myDCPower.set_voltage(24), myDCPower.heromix.query('VOLT?'))
    # print('设置电流', myDCPower.set_current(1), myDCPower.heromix.query('CURR?'))
    # #print('查询设定电压电流', myDCPower.heromix.query('APPL?'))
    # sleep(0.5)
    # print('查询真实的输出电压', myDCPower.get_measure_voltage(), myDCPower.get_fetch_voltage())
    # print('查询真实的输出电流', myDCPower.get_measure_current(), myDCPower.get_fetch_current())
    # sleep(2)
    # myDCPower.output('OFF')


if __name__ == "__main__":
    main()
