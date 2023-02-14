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
        self.meas_out = [""] * 3
        self.u_wkmode = {
            'Vin': 1,  # 直流电源电压设置
            'Iin': 0.001,
            '序号': 1,
            'Freq': 1000,
            'Volt': 1,
            'Path': "E:/",
        }
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化测试架
        ATS.myCraft.setChan([False] * 32)
        ATS.setDCPowerOnOff('OFF')
        # 初始化DC电源
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 测试架测试通道设置
        do = [False] * 32
        # index = (self.u_wkmode['序号'] - 1) % 14
        index = 0
        do[index] = [True]
        do[index + 16] = [True]
        do[30] = [True]
        ATS.myCraft.setChan(do)
        sleep(0.5)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # meas_out[0]：二极管正向压降V-F
            # meas_out[1]：二极管正向电流I-F
            # meas_out[2]：二极管测试状态
            Volt_test = ATS.myDMM.get_dc_val()
            Curr_test = ATS.getDCPowerMeasCurr()
            if Curr_test < self.u_wkmode["Iin"] * 0.95:  # 电源未工作在电流源模式
                if Curr_test < self.u_wkmode["Iin"] * 0.1:  # 二极管开路
                    self.meas_out[2] = "开路"
                else:
                    self.meas_out[2] = "欠压"  # 电源测试电压偏小

            else:
                if Volt_test > self.u_wkmode["Vin"] * 0.95:
                    self.meas_out[2] = "欠压"  # 电源测试电压偏小
                else:
                    self.meas_out[0] = round(Volt_test, 3)
                    self.meas_out[1] = round(Curr_test, 3)
                    self.meas_out[2] = "OK"

            # 测试结束，初始化测试架，DC电源
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
