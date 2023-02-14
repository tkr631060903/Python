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
            'Iin': 0.001,
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
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(1)
        ATS.setEloadCCval(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')
        ATS.setEloadOnOff('ON')
        sleep(1)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # meas_out[0]:输出电压；
            # meas_out[1]:导通电阻；
            # meas_out[2]:负载电流；

            self.meas_out[2] = round(ATS.getEloadMeasCurr(), 3)
            # Volt_DC = round(ATS.getDCPowerMeasVolt(), 3)
            # Volt_Eload = round(ATS.getEloadMeasVolt(), 3)
            Volt_DMM = round(ATS.myDMM.get_dc_val(), 3)
            # self.meas_out[0] = Volt_DC - Volt_DMM
            self.meas_out[0] = round(
                ATS.getDCPowerMeasVolt() - ATS.myDMM.get_dc_val(), 3)
            if self.meas_out[2] <= 0:
                self.meas_out[1] = "ERR"
            else:
                self.meas_out[1] = ATS.uint(Volt_DMM / self.meas_out[2], "Ω")

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
