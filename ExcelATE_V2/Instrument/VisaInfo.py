#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa


class VisaInfo():
    """
    获取仪器信息
    """

    def getInstrumentNum():
        """
        获取仪器编号
        Arguments : None
            returns : my_instrument -- 仪器编号
        """
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())
        # dev = rm.list_resources()
        # dev = str(dev)
        # dev = dev.replace("(", "").replace(")", "",).replace("'", "",).replace(",", "",)
        if not rm.list_resources() == "()":
            for dev in rm.list_resources():
                my_instrument = rm.open_resource(dev)
                print(my_instrument.query("*IDN?"))
                # print(my_instrument)
                return my_instrument
        # my_instrument = rm.open_resource('USB0::0x2EC7::0x6700::802259072737410114::INSTR')
        # print(my_instrument)



if __name__ == "__main__":
    VisaInfo.getInstrumentNum()
