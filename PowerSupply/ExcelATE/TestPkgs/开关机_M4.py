# coding: utf-8
import sys
from corelib.autolib import ATS
from time import clock
import os

from corelib.config import Config
from corelib.immsg import IMMsg


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 11
        self.u_wkmode = {
            'Vin': 20,  # 直流电源电压设置
            'Iin': 1,
            '超时': 20,
            '间隔': 5,
            'Path': "D:/",
        }
        config = Config()
        self.st_clk = clock()
        self.cfg = config.getCfgMsg()
        self.msg = IMMsg(self.cfg)
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        self.meas_out[0] = "0"
        ATS.setDCPowerOnOff('OFF')
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        try:
            ATS.setDCPowerOnOff('OFF')
            st_clk = clock()
            i = 0
            while clock() - st_clk < self.u_wkmode['间隔']:
                if clock() - st_clk > i:
                    i += 1
                    print(
                        '\u001b[0K' + "[process]" + "第" +
                        str(mode + 1) + "次测试，预计" + str(
                            int(self.u_wkmode['间隔'] + 1 - i)) + "S后启动",
                        end='\r')
                    if i == self.u_wkmode['间隔'] - 1:
                        ATS.myScope.set_single()
            ATS.setDCPowerOnOff('ON')
        except Exception as err:
            print("[err] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            st_clk = clock()
            i = 0
            while clock() - st_clk < self.u_wkmode['超时']:
                if clock() - st_clk > i:
                    i += 1
                    str_total = ""
                    print(
                        '\u001b[0K' + "[process]" + "第" + str(mode + 1) +
                        "次测试，预计" + str(int(self.u_wkmode['超时'] + 1 - i)) +
                        "S后重启" + str_total,
                        end='\r')
            curr = ATS.getDCPowerMeasCurr()
            if curr < 0.08:
                image = ATS.getScopeScreen(self.u_wkmode['Path'] + '/Image',
                                           "-启动波形")
                msg = {
                    "action":
                    "终止",
                    "msg": [
                        "M4开关机第" + str(mode + 1) + "次测试启动异常",
                        self.u_wkmode['Path'] + "/Image/" + image
                    ]
                }
                self.msg.send(msg)
                os._exit(0)
            if mode % 20 == 19:
                msg = {
                    "action": "完成",
                    "msg": "M4开关机第" + str(mode + 1) + "次测试正常启动"
                }
                self.msg.send(msg)
        except Exception as err:
            print("[err] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    i = 0
    while True:
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
        i += 1
