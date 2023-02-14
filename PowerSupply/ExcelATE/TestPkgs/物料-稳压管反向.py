# coding: utf-8
import sys
from corelib.autolib import ATS
from time import sleep


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 5
        self.u_wkmode = {
            'Vin': 1,  # 直流电源电压设置
            'Iin': 0.001,  # 直流电源限流设置 
            '序号': 1,
            'Freq': 1000,
            'Volt': 1,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化DC电源，测试架
        ATS.setDCPowerOnOff('OFF')
        do = [False] * 32
        ATS.myCraft.setChan(do)

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 测试架测试通道设置
        do = [False] * 32
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        # do[index + 16] = [True]
        # do[31] = [True]
        ATS.myCraft.setChan(do)
        sleep(0.2)  # 延时200ms，保证电源2正常建压

        # DC电源测试参数设置
        ATS.setDCPowerVolt(self.u_wkmode['Vin'] / 0.7)
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')
        sleep(1)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 钳位测试电压下，稳压管钳位电压：meas_out[1]
            # self.meas_out[1] = ATS.uint(ATS.getDCPowerMeasVolt(), "V")

            # 钳位测试电压下，稳压管漏电流：meas_out[2]
            curr = ATS.myDMM.get_dc_curr()
            if curr < 0.0:
                curr = 0.0
            # self.meas_out[2] = ATS.uint(curr, "A")
            self.meas_out[1] = round(ATS.getDCPowerMeasVolt(), 3)
            self.meas_out[2] = round(curr, 3)

            # 漏电流测试电压下，稳压管漏电流：meas_out[0]
            ATS.setDCPowerVolt(self.u_wkmode['Vin'] *
                               0.7)  # 漏电流测试电压 = 钳位测试电压 / 2
            sleep(1)
            curr = ATS.myDMM.get_dc_curr()
            if curr < 0.0:  # 稳压管状态：开路
                curr = 0.0
            elif curr < 0.000000001:  # 稳压管漏电流精度：1nA
                curr = 0.000000001
            # self.meas_out[0] = ATS.uint(curr, "A")
            self.meas_out[0] = round(curr * 1000000, 3)  # 漏电流单位为uA

            # 测试完毕，初始化DC电源，测试架
            ATS.myCraft.setChan([False] * 32)
            ATS.setDCPowerOnOff('OFF')

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '万用表', 'CRAFT']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
