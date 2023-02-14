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
            'Vin': 12,
            'Iin': 2,
            '序号': 14,
            'Freq': 1000,   # LCR电桥测试频率设置
            'Volt': 1,  # LCR电桥测试电压设置
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)


    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化测试架
        do = [False] * 32
        ATS.myCraft.setChan(do)  
        sleep(0.1)        


    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 测试架测试通道设置
        do = [False] * 32
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        do[index + 16] = [True]
        ATS.myCraft.setChan(do)        
        sleep(0.1)


    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 电容值：meas_out[0]；
            # ESR值：meas_out[1]；
            self.meas_out[0] = ATS.myLCR.get_measure_val(
                "CSRS", self.u_wkmode['Freq'], self.u_wkmode['Volt'])[0]
            self.meas_out[1] = ATS.myLCR.get_measure_val(
                "CSRS", 200000, 0.5)[1]
            self.meas_out[0] = ATS.uint(self.meas_out[0], "F", 1)
            self.meas_out[1] = ATS.uint(self.meas_out[1])

            # 测试结束，初始化测试架
            ATS.myCraft.setChan([False] * 32)

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ['LCR', 'CRAFT']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
