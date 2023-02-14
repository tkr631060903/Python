# coding: utf-8
import sys
from corelib.autolib import ATS
from time import sleep

from corelib.config import Config
from corelib.immsg import IMMsg


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 8
        self.u_wkmode = {
            'Vin': 1.8,  # 直流电源电压设置
            'MHz': 0.5,  # 晶振参考频率设置
            '序号': 14,
            'Path': "E:/",
        }
        config = Config()
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)
        self.cfg = config.getCfgMsg()
        self.msg = IMMsg(self.cfg)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化数字电源
        ATS.setDCPowerOnOff('OFF')

        # 初始化示波器
        ATS.myScope.set_measure_clear()
        ATS.myScope.add_measure(1, "FREQ")
        ATS.myScope.add_measure(1, "MAX")
        ATS.myScope.add_measure(1, "DELAY")
        ATS.myScope.add_measure(1, "DUTY")
        ATS.myScope.set_resolution(100000)

        # 初始化测试架
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
        do[31] = [True]
        ATS.myCraft.setChan(do)

        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])

        # 使能示波器，DC电源
        ATS.setDCPowerOnOff('ON')
        sleep(1)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 晶振起振频率：meas_out[0]
            # 晶振起振占空比：meas_out[1]
            # 晶振起振功耗：meas_out[2]
            # 晶振起振延时：meas_out[3]
            ATS.myScope.set_timebase(0.001 / self.u_wkmode['MHz'], 30)
            ATS.myScope.set_run()
            sleep(0.1)
            do = [False] * 32
            index = (self.u_wkmode['序号'] - 1) % 14
            do[index] = [True]
            do[31] = [True]
            ATS.myCraft.setChan(do)

            ATS.myScope.set_stop()
            self.meas_out[3] = ATS.uint(
                ATS.myScope.get_measure_val(1, "DELAY"), "s")

            ATS.myScope.set_timebase(0.0000002 / self.u_wkmode['MHz'], 50)
            ATS.myScope.set_run()
            sleep(0.1)
            ATS.myScope.set_stop()
            freq = [0.0] * 12
            for i in range(12):
                freq[i] = ATS.myScope.get_measure_val(1, "FREQ")
            freq.sort()
            freq_sum = 0.0
            for i in range(10):
                freq_sum += freq[i + 1]
            self.meas_out[0] = ATS.uint(freq_sum / 10, "Hz")
            self.meas_out[1] = ATS.myScope.get_measure_val(1, "DUTY")
            self.meas_out[2] = ATS.uint(ATS.getDCPowerMeasCurr(), "A")

            # 测试结束，初始化DC电源、测试架
            ATS.setDCPowerOnOff('OFF')
            ATS.myCraft.setChan([False] * 32)

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ["直流电源", 'CRAFT']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
