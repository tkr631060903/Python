# coding: utf-8
import sys
from corelib.autolib import ATS
from time import clock


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 4

        self.u_wkmode = {
            'Vin': 12,  # 直流电源电压设置
            'Iin': 5,
            'Vmax': 24,
            'Vdrop': 4.5,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V Vmax:" +
              str(self.u_wkmode['Vmax']) + "V 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            pass
            ATS.setDCPowerOnOff('OFF')
            points = []
            for i in range(30):
                points.append("{0},2.49,0,0.011".format(
                    round(24 - ((24 - 12) * (i + 1) / 30), 3)))
            ATS.myDCPower.set_list({"index": 0, "repeat": 1, "points": points})
            points = []
            for i in range(30):
                points.append("{0},2.49,0,0.3".format(
                    round(12 + ((24 - 12) * (i + 1) / 30), 3)))
            ATS.myDCPower.set_list({"index": 1, "repeat": 1, "points": points})
            print("[process] init")
        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 设置其他工作条件，如改变设备状态，加入延时等等
        # ATS.setNI9472DO('0:5', [True] + [False]*4 + [True])
        try:
            pass
            # ATS.setDCPowerOnOff('ON')
            # for i in range(300):
            #     print("[process] run ",i)
            #     ATS.myDCPower.set_list_run([0])
            #     ATS.myDCPower.set_list_run([1])

            # # ATS.setDCPowerOnOff('ON')
            # ATS.setDCPowerOnOff('OFF')
        except Exception as err:
            print("[process] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
           pass
        except Exception as err:
            print("[process] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
