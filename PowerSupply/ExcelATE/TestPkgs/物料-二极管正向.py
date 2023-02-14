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
            '序号': 1,
            'Freq': 1000,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化测试架，DC电源
        do = [False] * 32
        ATS.myCraft.setChan(do)
        ATS.setDCPowerOnOff('OFF')

        # 测试架基准通道（14）电流压降测试
        do[13] = [True]  # 基准通道（14）开通
        #do[14] = [True]  # 电源通道（15）开通
        ATS.myCraft.setChan(do)
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')
        sleep(0.2)
        self.ref = ATS.myDMM.get_dc_val()

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 测试架测试通道设置
        do = [False] * 32
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        ATS.myCraft.setChan(do)
        sleep(0.2)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 二极管正向压降值：meas_out[0]；
            self.Volt = ATS.myDMM.get_dc_val()
            self.Curr = ATS.getDCPowerMeasCurr()
            if self.Volt > 0.95 * self.u_wkmode['Vin']:  # DC电源未进入限流模式
                self.meas_out[0] = "ERR"
            else:
                # self.meas_out[0] = ATS.uint(self.Volt - self.ref, "V")
                self.meas_out[0] = round(self.Volt - self.ref, 3)

            # self.meas_out[1] = ATS.uint(self.Curr, "A")
            self.meas_out[1] = round(self.Curr, 3)

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
