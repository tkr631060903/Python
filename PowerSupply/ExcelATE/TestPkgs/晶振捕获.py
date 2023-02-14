# coding: utf-8
import sys
from corelib.autolib import ATS
from time import sleep
import os

from corelib.immsg import IMMsg
from corelib.config import Config
from corelib.capture import Capture


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 11
        self.u_wkmode = {
            'Vin': 12,  # 直流电源电压设置
            'Iin': 2.4,
            '等待': 3,
            'Path': "E:/ExcelATE/DV实验",
        }
        config = Config()
        self.capture = None
        self.cfg = config.getCfgMsg()
        self.msg = IMMsg(self.cfg)
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        self.meas_out[0] = 0
        ATS.setDCPowerOnOff('OFF')
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        self.capture = Capture(ATS.myScope)

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        try:
            ATS.myScope.set_run()
            ATS.setDCPowerOnOff('OFF')
            sleep(1)
            ATS.setDCPowerOnOff('ON')
            sleep(self.u_wkmode['等待'])
        except Exception as err:
            print("[err] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            print("[process]" + "第" + str(mode + 1) + "次测试")
            result = self.capture.tryCapture(self.u_wkmode['Path'])
            action = result[0]
            if action is not "":
                msg = {
                    "action":
                    action,
                    "msg":
                    [self.u_wkmode['Path'] + "/Image/" + result[2], result[1]]
                }
                self.msg.send(msg)
            if action.find("终止") >= 0:
                os._exit(0)
            self.meas_out = result[3:]
        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    num = 9000
    for i in range(num):
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
    msg = {"action": "完成", "msg": "晶振" + str(num) + "次测试完成"}
    ate.msg.send(msg)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
