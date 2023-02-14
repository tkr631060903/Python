# coding: utf-8
import sys
from corelib.autolib import ATS
from time import sleep
import numpy


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 8
        self.u_wkmode = {
            'Vin': 1,  # 直流电源电压设置
            'Iin': 0.1,
            '序号': 1,
            'Freq': 1000,
            'Volt': 1,
            'Path': "E:/",
            "Res": 1
        }
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化测试DC电源，电子负载
        ATS.myAuxDCPower.set_batt_mode('DISCharge')
        ATS.myAuxDCPower.set_batt_voltage(7.4)
        ATS.setDCPowerOnOff('OFF')

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 使能DC电源
        # 防止上电过充，损坏电源IC，先以低压1V启动数字电源
        ATS.myAuxDCPower.set_batt_status('STARt')
        for val in numpy.arange(7.4, 8.2, 0.1):
            ATS.myAuxDCPower.set_batt_voltage(val)
            sleep(0.5)
            print(ATS.getDCPowerMeasCurr(), 'A')
        for val in numpy.arange(8.2, 8.4, 0.02):
            ATS.myAuxDCPower.set_batt_voltage(val)
            sleep(0.5)
            print(ATS.getDCPowerMeasCurr(), 'A')
        ATS.myAuxDCPower.set_batt_voltage(7.4)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        pass


if __name__ == "__main__":
    # use_devices = ['直流电源:IT67', '辅助电源:["IT61","IT64"]', "万用表", 'CRAFT']
    # use_devices = ['直流电源:IT67', '辅助电源:["IT64"]']
    use_devices = ['辅助电源:["IT64"]']

    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
