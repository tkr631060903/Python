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
        ATS.setDCPowerOnOff('OFF')
        ATS.setEloadOnOff('OFF')

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 使能DC电源
        # 防止上电过充，损坏电源IC，先以低压1V启动数字电源
        ATS.setDCPowerVolt(1)
        ATS.setDCPowerCurr(5)
        ATS.setDCPowerOnOff('ON')
        sleep(0.2)
        # 使能DC电源
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(5)
        ATS.setDCPowerOnOff('ON')
        sleep(0.5)
        ATS.setEloadCCval(self.u_wkmode['Iin'])
        ATS.setEloadOnOff('ON')
        sleep(0.5)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # meas_out[0]:输入电压；
            # meas_out[1]:输入电流；
            # meas_out[2]:输出电压；
            # meas_out[3]:输出电流；
            # meas_out[4]:效率值；
            self.meas_out[0] = round(ATS.getDCPowerMeasVolt(), 3)
            self.meas_out[1] = round(ATS.getDCPowerMeasCurr(), 3)
            # self.meas_out[2] = round(ATS.getEloadMeasVolt(), 3)
            self.meas_out[2] = round(ATS.myDMM.get_dc_val(), 3)
            self.meas_out[3] = round(ATS.getEloadMeasCurr(), 3)
            if self.meas_out[0] <= 0 or self.meas_out[1] <= 0:
                self.meas_out[4] = 0
            else:
                self.meas_out[4] = round(
                    100 * (self.meas_out[2] * self.meas_out[3]) /
                    (self.meas_out[0] * self.meas_out[1]), 3)
            # 测试结束，初始化DC电源，电子负载
            ATS.setDCPowerOnOff('OFF')
            ATS.setEloadOnOff('OFF')

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    # use_devices = ['直流电源:IT67', '辅助电源:["IT61","IT64"]', "万用表", 'CRAFT']
    use_devices = [
        "直流电源",
        "万用表",
        "电子负载",
    ]
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
