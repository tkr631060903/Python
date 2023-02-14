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
            'Iin': 0.1,  # 直流电源限流设置
            '序号': 14,
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

        # 初始化测试架，DC电源
        ATS.myCraft.setChan([False] * 32)
        ATS.setDCPowerOnOff('OFF')

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 使能DC电源
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')

        # 测试架测试通道设置
        do = [False] * 32
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        # do[31] = [True]   # 电源2使能
        ATS.myCraft.setChan(do)
        sleep(0.5)  # 延时200ms，保证电源2正常建压

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 二极管漏电流：meas_out[0]；
            curr = ATS.myDMM.get_dc_curr()
            Volt = ATS.getDCPowerMeasVolt()
            if curr < 0.0:  # 二极管状态：开路
                curr = 0.0
            elif curr < 0.000000001:  # 二极管漏电流精度：1nA
                curr = 0.000000001
            # self.meas_out[0] = ATS.uint(curr, "A")
            self.meas_out[0] = round(curr * 1000000, 3)  # 漏电流单位为uA
            # self.meas_out[1] = ATS.uint(Volt, "V")
            self.meas_out[1] = round(Volt, 3)

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
