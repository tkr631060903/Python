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
            "Res": 1  # 三极管b极电流采样电阻值：1k
        }
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化测试DC电源
        ATS.setDCPowerOnOff('OFF')
        ATS.setAuxDCPowerOnOff('OFF')

        # 初始化测试架
        do = [False] * 32
        ATS.myCraft.setChan(do)

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 使能DC电源
        ATS.setDCPowerVolt(0)
        ATS.setDCPowerCurr(0.1)
        ATS.setAuxDCPowerVolt(1)
        ATS.setAuxDCPowerCurr(0.1)
        ATS.setAuxDCPowerOnOff('ON')
        ATS.setDCPowerOnOff('ON')

        # 测试架测试通道设置
        do = [False] * 32
        do[30] = [True]  # 电源1使能
        do[31] = [True]  # 电源2使能
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        do[index + 16] = [True]
        ATS.myCraft.setChan(do)

        sleep(1)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 三极管β值：meas_out[0]；
            curr_o = 0
            val_i = 0.4
            while curr_o < 0.01:  # 按照Ic = 10mA指标，测量三极管β值
                val_i += 0.01
                ATS.setDCPowerVolt(val_i)
                sleep(0.4)
                curr_o = ATS.getAuxDCPowerMeasCurr()
                if val_i > self.u_wkmode["Res"] * 2:  # 测量三极管β值，扫描电压上限:2V
                    print("[process]" + str(self.u_wkmode['序号']) + "#电压:" +
                          str(val_i) + "V,超出限值,中断测试")
                    return
            val = ATS.myDMM.get_dc_val()
            self.meas_out[0] = int(curr_o / (val_i - val) *
                                   self.u_wkmode["Res"] * 1000)

            # 三极管I-c值：meas_out[1]；
            # self.meas_out[1] = ATS.uint(curr_o, "A", 2)
            self.meas_out[1] = round(curr_o, 3)

            # 三极管V-be值：meas_out[2]；
            val_i = 5 * self.u_wkmode["Res"] + val_i
            val = val_i
            while val_i - val < 5 * self.u_wkmode["Res"]:
                val_i += 0.01
                ATS.setDCPowerVolt(val_i)
                val = ATS.myDMM.fetc()
                if val_i > self.u_wkmode["Res"] * 8:  # 测量三极管Vbe值，扫描电压上限:8V
                    print("[process]" + str(self.u_wkmode['序号']) + "#电压:" +
                          str(val_i) + "V,超出限值,中断测试")
                    return
            # self.meas_out[2] = ATS.uint(val, "V", 2)
            self.meas_out[2] = round(val, 3)

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
