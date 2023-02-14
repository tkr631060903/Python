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
            'Iin': 0.1,
            '序号': 1,
            'Freq': 1000,
            'Volt': 1,
            'Time': 1,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        self.meas_out[0] = 0

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
        # 使能电源
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # LED开关机失败计数：meas_out[0]；

            # 测试架测试通道设置
            do = [False] * 32
            index = (self.u_wkmode['序号'] - 1) % 14
            do[index] = [True]
            do[index + 16] = [True]
            do[30] = [True]
            ATS.myCraft.setChan(do)
            sleep(0.1)
            self.val_cmp = ATS.myDMM.get_dc_val()

            for i in range(0, 500 * self.u_wkmode['Time']):
                ATS.setDCPowerOnOff('ON')
                sleep(0.2)

                val = ATS.myDMM.get_dc_val()
                if val > self.val_cmp * 1.1 or val < self.val_cmp * 0.9:
                    self.meas_out[0] += 1
                # print('\u001b[0K' + "[process]" + "第" + str(mode + 1) +
                #   "次测试，已检测" + str(self.meas_out[1]) + "次异常",
                #   end='\r')

                print('\u001b[0K' + "[process]" + "第" +
                      str(self.u_wkmode['序号']) + "组测试，" + "第" + str(i + 1) +
                      "次测试，" + str(self.meas_out[0]) + "次异常",
                      end='\r')

                ATS.setDCPowerOnOff('OFF')
                sleep(0.2)
            # self.meas_out[0] = ATS.uint(ATS.myDMM.get_dc_val() - self.ref, "V")
            # ATS.myCraft.setChan( [False] * 32)

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
    # for i in range(500):
    #     ate.U_SetStatus(i)
    #     ate.U_GetDatas(i)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
