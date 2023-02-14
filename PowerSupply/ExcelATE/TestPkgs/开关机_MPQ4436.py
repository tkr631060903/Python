# coding: utf-8
import sys
from corelib.autolib import ATS
from time import clock, sleep

if __name__ == "__main__":
    use_devices = ['直流电源', '电子负载']
    ATS.connect_devices(use_devices)
    l_loadcurrent = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    num = 0
    ATS.setDCPowerOnOff('OFF')
    ATS.setEloadOnOff('OFF')
    ATS.setDCPowerVolt(24)
    ATS.setDCPowerCurr(5)
    ATS.myEload.set_mode('CURR')
    while True:
        for i in range(len(l_loadcurrent)):
            ATS.myEload.set_current(l_loadcurrent[i])
            ATS.setDCPowerOnOff('ON')
            ATS.setEloadOnOff('ON')
            sleep(5)
            curr_source = ATS.getDCPowerMeasCurr()
            curr_load = ATS.myEload.get_measure_current()
            volt_load = ATS.myEload.get_measure_voltage()
            if (curr_load > 0.9*l_loadcurrent[i]) and (curr_source >
                                                   0.3 * l_loadcurrent[i]):
                pass                                
            else:
                print(f'未开机，一级电源输出电压为{volt_load}V，电源电流为{curr_source}A')

            ATS.setDCPowerOnOff('OFF')
            ATS.setEloadOnOff('OFF')
            sleep(5)
        num=num +len(l_loadcurrent)
        print(f'总开关机次数为{num}')