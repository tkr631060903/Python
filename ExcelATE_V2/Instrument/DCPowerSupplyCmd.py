#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pyvisa
from threading import RLock

from Instrument.VisaInfo import VisaInfo


class DCPowerSupplyCmd():
    """
    直流电源控制类
    """

    def __init__(self):
        self.xlock = RLock()

    def IDN(my_instrument):
        """获取仪器ID名称
        arguments : my_instrument -- 仪器编号
            returns : info -- IDN
        """
        info = my_instrument.query('*IDN?')
        return info

    def set_switch(my_instrument, onoff):
        """打开/关闭电源
        arguments : my_instrument -- 仪器编号, onoff -- ON/OFF(开/关)
            returns : rstatus 
        """
        rstatus = my_instrument.write('OUTP {0}'.format(onoff))
        return rstatus

    #电流指令
    def set_current(my_instrument, current):
        """设定电源输出电流
        arguments : my_instrument -- 仪器编号, current -- 电流(A)
            returns : rstatus 
        """
        # self.xlock.acquire()
        rstatus = my_instrument.write('CURR {0}'.format(current))
        # self.xlock.release()
        return rstatus

    def set_current_step(my_instrument, step):
        """设定电流输出步进
        arguments : my_instrument -- 仪器编号, step -- 电流步进(A)
            returns : rstatus 
        """
        rstatus = my_instrument.write('CURR:STEP {0}'.format(step))
        return rstatus

    def set_current_trig(my_instrument, current):
        """设定等待触发的电流值
        arguments : my_instrument -- 仪器编号, current -- 等待触发电流(A)
            returns : rstatus 
        """
        rstatus = my_instrument.write('CURR:TRIG {0}'.format(current))
        return rstatus

    def set_current_port(my_instrument, current):
        """设定过电流保护值
        arguments : my_instrument -- 仪器编号, current -- 保护电流(A)
            returns : rstatus 
        """
        rstatus = my_instrument.write('CURR:PROT {0}'.format(current))
        return rstatus

    def set_current_port_state(my_instrument, onoff):
        """打开或关闭OCP功能, 即设定过流保护状态
        arguments : my_instrument -- 仪器编号, current -- ON/OFF(开/关)
            returns : rstatus 
        """
        rstatus = my_instrument.write('CURR:PROT:STAT {0}'.format(onoff))
        return rstatus

    def set_current_up(my_instrument):
        """使输出电流增加一次
        arguments : my_instrument -- 仪器编号
            returns : rstatus 
        """
        rstatus = my_instrument.write("CURR UP")
        return rstatus

    #电压指令
    def set_voltage(my_instrument, voltage):
        """设定电压输出电压
        arguments : my_instrument -- 仪器编号, voltage -- 电压(V)
            returns : rstatus 
        """
        rstatus = my_instrument.write('VOLT {0}'.format(voltage))
        return rstatus

    def set_voltage_step(my_instrument, step):
        """设定电压输出步进
        arguments : my_instrument -- 仪器编号, step -- 步进(V)
            returns : rstatus 
        """
        rstatus = my_instrument.write('VOLT:STEP {0}'.format(step))
        return rstatus

    def set_voltage_trig(my_instrument, voltage):
        """设定等待触发的电压值
        arguments : my_instrument -- 仪器编号, voltage -- 等待触发电压(V)
            returns : rstatus 
        """
        rstatus = my_instrument.write('VOLT:TRIG {0}'.format(voltage))
        return rstatus

    def set_voltage_prot(my_instrument, voltage):
        """设定过电压保护值
        arguments : my_instrument -- 仪器编号, voltage -- 保护电压(V)
            returns : rstatus 
        """
        rstatus = my_instrument.write('VOLT:PROT {0}'.format(voltage))
        return rstatus

    def set_voltage_prot_state(my_instrument, onoff):
        """打开或关闭OCP功能, 即设定过压保护状态
        arguments : my_instrument -- 仪器编号, voltage -- ON/OFF(开/关)
            returns : rstatus 
        """
        rstatus = my_instrument.write('VOLT:PROT:STAT {0}'.format(onoff))
        return rstatus

    def set_voltage_limit(my_instrument, voltage):
        """设定电压上限值
        arguments : my_instrument -- 仪器编号, voltage -- 电压(V)
            returns : rstatus 
        """
        rstatus = my_instrument.write('VOLT:LIMIT {0}'.format(voltage))
        return rstatus

    def set_voltage_up(my_instrument):
        """使输出电压增加一次
        arguments : my_instrument -- 仪器编号
            returns : rstatus 
        """
        rstatus = my_instrument.write("VOLT UP")
        return rstatus

    #测量指令
    def get_measure_current(my_instrument):
        """检测并返回当前的电流值
        arguments : my_instrument -- 仪器编号
            returns : current -- 返回电流值 
        """
        current = my_instrument.query('MEAS:CURR?')
        return float(current)

    def get_fetch_current(my_instrument):
        """从缓存区读取最近的电流值
        arguments : my_instrument -- 仪器编号
            returns : current -- 返回电流值 
        """
        current = my_instrument.query('FETC:CURR?')
        return float(current)

    def get_measure_voltage(my_instrument):
        """检测并返回当前的电压值
        arguments : my_instrument -- 仪器编号
            returns : voltage -- 返回电压值 
        """
        voltage = my_instrument.query('MEAS:VOLT?')
        return float(voltage)

    def get_fetch_voltage(my_instrument):
        """从缓存区读取最近的电压值
        arguments : my_instrument -- 仪器编号
            returns : voltage -- 返回电压值 
        """
        voltage = my_instrument.query('FETC:VOLT?')
        return float(voltage)

    def get_measure_power(my_instrument):
        """检测并返回当前的功率值
        arguments : my_instrument -- 仪器编号
            returns : power -- 返回功率值
        """
        power = my_instrument.query('MEAS:POW?')
        return float(power)

    def get_fetch_power(my_instrument):
        """从缓存区读取最近的功率值
        arguments : my_instrument -- 仪器编号
            returns : power -- 返回功率值 
        """
        power = my_instrument.query('FETC:POW?')
        return float(power)


def main():
    my_instrument = VisaInfo.getInstrumentNum()
    DCPowerSupplyCmd.set_switch(my_instrument, "ON")


if __name__ == "__main__":
    main()
    # my_instrument = VisaInfo.getInstrumentNum()
    # DCPowerSupplyCmd.set_switch(my_instrument, "ON")
    # DCPowerSupplyCmd.set_current(my_instrument, 1)
    # DCPowerSupplyCmd.set_voltage(my_instrument, 1)
    # val = DCPowerSupplyCmd.get_measure_voltage(my_instrument)
    # val1 = DCPowerSupplyCmd.get_fetch_voltage(my_instrument)
    # print(val)
    # print(val1)
