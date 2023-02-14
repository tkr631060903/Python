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
        self.meas_out = [""] * 6

        self.u_wkmode = {
            'Vin': 24,  # 直流电源电压设置
            'Iin': 2,
            'Iout': 0,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('OFF')
            ATS.myScope.set_resolution(100000)
            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.setDCPowerCurr(self.u_wkmode['Iin'])
            ATS.myScope.set_channel(1, "ON", "DC", 0.5, -3)
            ATS.myScope.set_channel(2, "ON", "DC", 0.5, -3)
            ATS.myScope.set_channel("CH1-CH2", "ON", "DC", 0.2, 0)
            ATS.myScope.set_timebase(50 / 1000.0, 50)
            ATS.myScope.set_measure_clear()
            ATS.myScope.add_measure("MATH", "AMP")
        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 设置其他工作条件，如改变设备状态，加入延时等等
        # ATS.setNI9472DO('0:5', [True] + [False]*4 + [True])
        if mode == 0:  # 启动测试
            try:
                ATS.myScope.set_trigger(1, "NORM", "RIS", 2)
                ATS.myScope.set_run()
                sleep(1)
                ATS.setDCPowerOnOff('ON')
                sleep(1)
                ATS.myScope.set_stop()
                sleep(2)
            except Exception as err:
                print("[process] set status error:" + str(err))
        elif mode == 1:  # 关机测试
            try:
                ATS.myScope.set_trigger(1, "NORM", "FALL", 0.5)
                ATS.myScope.set_run()
                sleep(1)
                ATS.setDCPowerOnOff('OFF')
                sleep(1)
                ATS.myScope.set_stop()
                sleep(2)
            except Exception as err:
                print("[process] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            if mode == 0:  # 启动测试
                self.meas_out[0] = round(ATS.getDCPowerMeasVolt(), 3)
                self.meas_out[1] = round(ATS.getDCPowerMeasCurr(), 3)
                self.meas_out[4] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-启动波形")
                float_tmp = ATS.myScope.get_measure_val("MATH", "AMP") * 1000.0
                if float_tmp < 10000:
                    self.meas_out[2] = round(float_tmp, 3)
            elif mode == 1:  # 关机测试
                self.meas_out[5] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-关机波形")
                float_tmp = ATS.myScope.get_measure_val("MATH", "AMP") * 1000.0
                if float_tmp < 10000:
                    self.meas_out[3] = round(float_tmp, 3)

            pass
        except Exception as err:
            print("[process] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    for i in range(2):
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
