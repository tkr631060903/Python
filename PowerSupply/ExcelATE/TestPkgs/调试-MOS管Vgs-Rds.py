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
            'Iin': 0.01,
            '序号': 1,
            'Freq': 1000,
            'Volt': 1,
            'Path': "E:/",
            "Res": 2
        }
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化测试DC电源、测试架
        ATS.setDCPowerOnOff('OFF')
        ATS.setAuxDCPowerOnOff('OFF')
        ATS.myCraft.setChan([False] * 32)

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 使能DC电源
        ATS.setDCPowerVolt(0.1)
        ATS.setDCPowerCurr(0.1)
        ATS.setAuxDCPowerVolt(0.1)
        ATS.setAuxDCPowerCurr(0.1)
        ATS.setAuxDCPowerOnOff('ON')
        ATS.setDCPowerOnOff('ON')
        sleep(0.1)

        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setAuxDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setAuxDCPowerCurr(self.u_wkmode['Iin'])

        # 测试架测试通道设置
        do = [False] * 32
        # index = (self.u_wkmode['序号'] - 1) % 14
        index = 0
        do[index] = [True]
        do[index + 16] = [True]
        do[30] = [True]  # 电源1使能
        do[31] = [True]  # 电源2使能
        ATS.myCraft.setChan(do)
        sleep(0.5)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # meas_out[0]：MOS管Vth-GS；
            # meas_out[1]：MOS管I-D；
            # meas_out[2]：MOS管V-DS；
            # meas_out[3]：MOS管R-DS；
            # meas_out[4]：MOS管测试状态；
            val_i = ATS.getDCPowerMeasVolt()
            curr_o = ATS.getAuxDCPowerMeasCurr()
            val_j = ATS.myDMM.get_dc_val()

            self.meas_out[0] = round(val_i, 3)
            self.meas_out[1] = ATS.uint(curr_o, "A")
            self.meas_out[2] = round(val_j, 3)
            if curr_o < 0.000000001:  # 电流精度：1nA
                curr_o = 0.000000001
                self.meas_out[3] = ""
            else:
                self.meas_out[3] = round(val_j / curr_o, 3)

            # 测试结束，初始化测试架，DC电源
            ATS.myCraft.setChan([False] * 32)
            ATS.setDCPowerOnOff('OFF')
            ATS.setAuxDCPowerOnOff('OFF')

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源:IT67', '辅助电源:["IT61","IT64"]', "万用表", 'CRAFT']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
