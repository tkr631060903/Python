# coding: utf-8
from corelib.autolib import ATS
from time import sleep
import math


class Wave():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def waveStart(self):
        for _un in (12, 24):
            for _type in (1, 2, 3, 4):
                if _un == 12:
                    tt, t6 = 0.005, 0.015
                    if _type == 1:
                        us, ua, t8, tf = 8, 9.5, 1, 0.04
                    elif _type == 2:
                        us, ua, t8, tf = 4.5, 6.5, 10, 0.1
                    elif _type == 3:
                        us, ua, t8, tf = 3, 5, 1, 0.1
                    elif _type == 4:
                        us, ua, t8, tf = 6, 6.5, 10, 0.1
                    start = 1 + (_type - 1) * 3
                elif _un == 24:
                    tt, t6 = 0.01, 0.05
                    if _type == 1:
                        us, ua, t8, tf = 10, 20, 1, 0.04
                    elif _type == 2:
                        us, ua, t8, tf = 8, 15, 10, 0.1
                    elif _type == 3:
                        us, ua, t8, tf = 6, 10, 1, 0.04
                    start = (_type - 1) * 3 + 11

                if _un == 24 and _type == 4:
                    pass
                else:
                    if _type == 4:
                        start = 0
                    print("[process]" + "@输入电压:" + str(_un) + "V 测试波形 TYPE:" +
                          str(_type))
                    points = []
                    points.append("{0},2.49,0,{1}".format(_un, 0.1))
                    for i in range(5):
                        points.append("{0},2.49,0,{1}".format(
                            round(_un - ((_un - us) * (i + 1) / 5), 3),
                            tt / 5))
                    points.append("{0},2.49,0,{1}".format(us, t6))
                    for i in range(10):
                        points.append("{0},2.49,0,{1}".format(
                            round(us + ((ua + 1 - us) * (i + 1) / 10), 3),
                            0.005))
                    ATS.myDCPower.set_list({
                        "index": start,
                        "repeat": 1,
                        "points": points
                    })
                    ATS.myDCPower.set_list_run([start])
                    sleep(1)
                    ATS.setDCPowerVolt(_un)

                    ATS.myDCPower.set_list({
                        "index": start,
                        "repeat": 1,
                        "points": points
                    })
                    ATS.myDCPower.set_list_run([start])
                    sleep(1)
                    ATS.setDCPowerVolt(_un)
                    if _type != 4:
                        points = []
                        for i in range(20):
                            points.append("{0},2.49,0,{1}".format(
                                round(ua + 1 - math.sin(2 * i * math.pi / 20),
                                      3), round(0.5 / 20, 3)))
                        ATS.myDCPower.set_list({
                            "index": start + 1,
                            "repeat": int(t8 * 2),
                            "points": points
                        })
                        ATS.myDCPower.set_list_run([start + 1])
                        sleep(t8 + 1)
                        ATS.setDCPowerVolt(_un)

                        ATS.myDCPower.set_list({
                            "index": start + 1,
                            "repeat": int(t8 * 2),
                            "points": points
                        })
                        ATS.myDCPower.set_list_run([start + 1])
                        sleep(t8 + 1)
                        ATS.setDCPowerVolt(_un)
                    if _type == 4:
                        start = 8
                    points = []
                    for i in range(20):
                        points.append("{0},2.49,0,{1}".format(
                            round(ua + 1 + ((_un - ua - 1) * (i + 1) / 20), 3),
                            tf / 20))
                    ATS.myDCPower.set_list({
                        "index": start + 2,
                        "repeat": 1,
                        "points": points
                    })
                    ATS.myDCPower.set_list_run([start + 2])
                    sleep(1)
                    ATS.setDCPowerVolt(_un)

                    ATS.myDCPower.set_list({
                        "index": start + 2,
                        "repeat": 1,
                        "points": points
                    })
                    ATS.myDCPower.set_list_run([start + 2])
                    sleep(1)
                    ATS.setDCPowerVolt(_un)

    def getWave(self, _un, _type):
        if _type < 4:
            if _un == 12:
                start = 1 + (_type - 1) * 3
            else:
                start = 11 + (_type - 1) * 3
            return [start, start + 1, start + 2]
        elif _type == 4:
            if _un == 12:
                return [0, 5, 10]

    def setWave(self, _un, _type):
        ATS.setDCPowerOnOff('ON')
        ATS.myDCPower.set_list_run(self.getWave(_un, _type))


if __name__ == "__main__":
    use_devices = ['直流电源', '示波器']
    ate = Wave()
    try:
        ATS.connect_devices(use_devices)
    except Exception as err:
        print("[process]" + str(err))
    cmd = input("'Enter'跳过波形配置\n任意键开始波形配置")
    if cmd != "":
        ate.waveStart()
        print("波形配置完成")
    cmd = input("'Enter'退出,输入'电压,类型'测试配置波形")
    while cmd != "":
        try:
            ate.setWave(int(cmd.split(',')[0]), int(cmd.split(',')[1]))
        except Exception:
            pass
        cmd = input("'Enter'退出,输入'电压,类型'测试配置波形")
    ATS.delete_devices(use_devices)
