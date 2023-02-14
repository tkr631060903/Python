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
        self.meas_out = [""] * 11

        self.u_wkmode = {
            'Vin': 24,  # 直流电源电压设置
            'Iin': 2,
            'Freq': 50,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 输入频率:" +
              str(self.u_wkmode['Freq'] / 1000) + "KHz 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('OFF')
            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.setDCPowerCurr(self.u_wkmode['Iin'])
            ATS.setDCPowerOnOff('ON')
            ATS.mySignalGen.set_source_apply_square(
                1, self.u_wkmode['Freq'] * 1000, 3, 1.5, 0)
            ATS.setSignalGenOnOff(1, "ON")
            ATS.myScope.set_resolution(100000)
            ATS.myScope.set_channel(1, "ON", "DC", 1, -2)
            ATS.myScope.set_channel(2, "ON", "DC", 1, -2)
            ATS.myScope.set_timebase(200 / 1000000.0 / self.u_wkmode['Freq'],
                                     50)
        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 设置其他工作条件，如改变设备状态，加入延时等等
        # ATS.setNI9472DO('0:5', [True] + [False]*4 + [True])
        if mode == 1:  # 正向测试
            try:
                ATS.myScope.set_measure_clear()
                ATS.myScope.set_trigger("EXT", "NORM", "FALL", 0.5)
                ATS.myScope.set_run()
                sleep(1)
                ATS.myScope.set_stop()
                ATS.myScope.set_channel("CH1-CH2", "ON", "DC", 1, -2)
                ATS.myScope.add_measure("MATH", "POV")
                ATS.myScope.add_measure("MATH", "RIS")
                sleep(2)

            except Exception as err:
                print("[process] set status error:", mode, err)
        elif mode == 0:
            try:
                ATS.myScope.set_trigger("EXT", "NORM", "RIS", 2)
                ATS.myScope.set_run()
                sleep(1)
                ATS.myScope.set_stop()
                ATS.myScope.set_measure_clear()
                ATS.myScope.add_measure("MATH", "NOV")
                ATS.myScope.add_measure("MATH", "FALL")
                sleep(2)
            except Exception as err:
                print("[process] set status error:", mode, err)
        elif mode == 2:
            try:
                ATS.myScope.set_measure_clear()
                ATS.setDCPowerOnOff('OFF')
            except Exception as err:
                print("[process] set status error:", mode, err)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            if mode == 1:
                float_tmp = ATS.myScope.get_measure_val("MATH", "POV")
                if float_tmp < 10000:
                    self.meas_out[8] = round(float_tmp, 3)
                float_tmp = ATS.myScope.get_measure_val("MATH",
                                                        "RIS") * 1000000000
                if float_tmp < 10000:
                    self.meas_out[6] = round(float_tmp, 3)
            elif mode == 0:
                float_tmp = ATS.myScope.get_measure_val("MATH",
                                                        "FALL") * 1000000000
                if float_tmp < 10000:
                    self.meas_out[7] = round(float_tmp, 3)
                float_tmp = ATS.myScope.get_measure_val("MATH", "NOV")
                if float_tmp < 10000:
                    self.meas_out[9] = round(float_tmp, 3)
            elif mode == 2:
                result = ATS.myScope.get_cursor_y(
                    [1, 2, "MATH"],
                    -1 / (self.u_wkmode['Freq'] * 1000 * 5 * 2),
                    1 / (self.u_wkmode['Freq'] * 1000 * 1.25 * 2))
                self.meas_out[0] = result[0][0]
                self.meas_out[1] = result[1][0]
                self.meas_out[2] = result[2][0]
                self.meas_out[3] = result[0][1]
                self.meas_out[4] = result[1][1]
                self.meas_out[5] = result[2][1]
                self.meas_out[10] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-波形")

        except Exception as err:
            print("[process] get data error:", mode, str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '信号源', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    for i in range(3):
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
