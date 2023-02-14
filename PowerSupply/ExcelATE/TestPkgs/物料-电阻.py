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

        # 初始化测试架
        do = [False] * 32

        # 测试架基准通道（14）电阻值测试
        do[13] = [True]
        do[13 + 16] = [True]
        ATS.myCraft.setChan(do)
        sleep(0.1)
        self.ref = ATS.myDMM.get_res()

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
            # 电阻值：meas_out[0]
            res = ATS.myDMM.get_res() - self.ref
            self.meas_out[0] = ATS.uint(res)
            ATS.myCraft.setChan([False] * 32)

            # ATS.setDCPowerOnOff('OFF')

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ['万用表', 'CRAFT']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
