#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pyvisa
import time

from Instrument.DCPowerSupplyCmd import DCPowerSupplyCmd
from Instrument.VisaInfo import VisaInfo


class Diode():
    """
    二极管测试类
    """

    def __init__(self):
        super().__init__()
        self.testStopComplete = False

    def init(my_instrument):
        """初始化电源
        arguments : my_instrument -- 仪器编号
            returns : None
        """
        DCPowerSupplyCmd.set_switch(my_instrument, "OFF")
        DCPowerSupplyCmd.set_current(my_instrument, 0)
        DCPowerSupplyCmd.set_voltage(my_instrument, 0)
        

    def TestRun(self, my_instrument, voltage, current):
        DCPowerSupplyCmd.set_voltage(my_instrument, 0)
        DCPowerSupplyCmd.set_current(my_instrument, current)
        DCPowerSupplyCmd.set_switch(my_instrument, "ON")
        DCPowerSupplyCmd.set_voltage_step(my_instrument, 0.1)
        time.sleep(0.5)
        status = (float(DCPowerSupplyCmd.get_fetch_voltage(my_instrument)))
        while status < voltage:
            DCPowerSupplyCmd.set_voltage_up(my_instrument)
            time.sleep(0.3)
            status = round(
                float(DCPowerSupplyCmd.get_fetch_voltage(my_instrument)), 1)
            print("当前电压值为：{} V".format(status))
            if (self.testStopComplete == True):
                break
        time.sleep(0.2)
        Diode.init(my_instrument)

    def main(self, voltage, current):
        my_instrument = VisaInfo.getInstrumentNum()
        print(my_instrument)
        Diode.init(my_instrument)
        Diode.TestRun(self, my_instrument, float(voltage), float(current))
        return True


if __name__ == "__main__":
    Diode.main()