#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa
import time

class DCPowerSupply():
    """
    直流电源类
    """
    def getDCPwoerInfo():
        """获取仪器ID名称
        arguments : None
            returns : my_instrument -- 仪器ID名称
        """
        rm = pyvisa.ResourceManager()
        # print(rm.list_resources())
        # dev = rm.list_resources()
        # dev = str(dev)
        # dev = dev.replace("(", "").replace(")", "",).replace("'", "",).replace(",", "",)
        for dev in rm.list_resources():
            pass
        # my_instrument = rm.open_resource('USB0::0x2EC7::0x6700::802259072737410114::INSTR')
        my_instrument = rm.open_resource(dev)
        # print(my_instrument)
        return my_instrument


    def DCPwoerControl(my_instrument, voltage, current):
        """控制直流电源
        arguments : my_instrument -- 仪器ID名称, voltage -- 电压上限, current -- 电流上限
            returns : None
        """
        devType = my_instrument.query("*IDN?")[11:18]   #获取程控电源型号
        my_instrument.write("CURR {0}".format(current))
        my_instrument.write("VOLT 0")
        my_instrument.write("OUTP ON")
        my_instrument.write("VOLT:STEP 0.1")
        time.sleep(0.5)
        status = (float(my_instrument.query("FETCh:VOLTage?")))
        # if devType == "IT6722A" or "IT6723A":
        #     cal = 0.1
        # else:
        #     cal = 0
        while status < voltage:
            my_instrument.write("VOLT UP")
            time.sleep(0.3)
            status = round(float(my_instrument.query("FETCh:VOLTage?")), 1)
            print("当前电压:{0}V".format(status))
        time.sleep(0.2)
        my_instrument.write("CURR 0")
        my_instrument.write("VOLT 0")
        my_instrument.write("OUTP OFF")
        # my_instrument.write("SYST:BEEP")
        return None


if __name__=="__main__":
    my_instrument = DCPowerSupply.getDCPwoerInfo()
    DCPowerSupply.DCPwoerControl(my_instrument, 2, 1)