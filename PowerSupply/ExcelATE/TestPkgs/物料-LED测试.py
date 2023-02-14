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
        self.meas_out = [""] * 5
        self.u_wkmode = {
            'Vin': 3.3,  # 直流电源电压设置
            'Iin': 0.02,
            '序号': 1,
            'Freq': 1000,
            'Volt': 1,
            'Time': 1,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        self.meas_out[2] = 0
        self.meas_out[3] = 0
        config = Config()
        ATS.getArgv(self.u_wkmode, sys.argv)
        self.cfg = config.getCfgMsg()
        self.msg = IMMsg(self.cfg)

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

        # 测试架测试通道设置
        do = [False] * 32
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        do[index + 16] = [True]
        do[30] = [True]
        ATS.myCraft.setChan(do)
        sleep(1.5)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # LED正向导通压降：meas_out[0]；
            # LED正向测试电流：meas_out[1]；
            # LED正向开关机失败次数：meas_out[2]；
            # LED正向开关机总次数：meas_out[3]；
            self.val = ATS.myDMM.get_dc_val()
            self.curr = ATS.getDCPowerMeasCurr()
            curr_temp = 0.0
            if self.curr >= 0.8 * self.u_wkmode['Iin']:
                # self.meas_out[0] = ATS.uint(self.val, "V")
                self.meas_out[0] = round(self.val, 3)
                self.sum = 500 * self.u_wkmode['Time']
                for i in range(0, self.sum):
                    ATS.setDCPowerOnOff('ON')
                    sleep(0.1)
                    val_temp = ATS.myDMM.get_dc_val()
                    if val_temp > self.val * 1.1 or val_temp < self.val * 0.9:
                        val_temp = ATS.myDMM.get_dc_val()
                        if val_temp > self.val * 1.1 or val_temp < self.val * 0.9:
                            self.meas_out[2] += 1
                            curr_temp = ATS.getDCPowerMeasCurr()
                            msg = {
                                "action":
                                "完成",
                                "msg":
                                "[" + str(self.u_wkmode['序号']) + "#] LED测试：" +
                                str(self.meas_out[2]) + "次异常,二极管导通基准电压为：" +
                                str(round(self.val, 3)) + "V,二极管实测电压为：" +
                                str(round(val_temp, 3)) + "V,电流为：" +
                                str(round(curr_temp * 1000, 3)) + "mA."
                            }
                            self.msg.send(msg)
                    # print('\u001b[0K' + "[process]" + "第" + str(mode + 1) +
                    #   "次测试，已检测" + str
                    print('\u001b[0K' + "[process]" + "第" +
                          str(self.u_wkmode['序号']) + "组测试，" + "第" +
                          str(i + 1) + "次测试，" + str(self.meas_out[2]) + "次异常",
                          end='\r')

                    ATS.setDCPowerOnOff('OFF')
                    sleep(0.1)

                    if i % 100 == 99:
                        try:
                            msg = {
                                "action":
                                "完成",
                                "msg":
                                "[" + str(self.u_wkmode['序号']) +
                                "#] LED测试：已完成" + "第" + str(i + 1) + "次测试，" +
                                str(self.meas_out[2]) + "次异常."
                            }
                            self.msg.send(msg)
                        except Exception as err:
                            print("[err] get status error:" + str(err))

                # self.meas_out[3] = self.sum
            else:
                self.meas_out[0] = "ERR"
            self.meas_out[3] = self.sum
            self.meas_out[1] = round(self.curr * 1000, 3)

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
