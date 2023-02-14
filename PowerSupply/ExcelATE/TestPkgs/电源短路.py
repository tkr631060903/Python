# coding: utf-8
import sys
from corelib.autolib import ATS
from time import clock, sleep


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 11
        self.u_wkmode = {
            'Vin': 8,  # 直流电源电压设置
            'Iin': 5,
            'Vout': 4,
            'Time': 10,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)

        if self.u_wkmode['Time'] < 10:
            self.u_wkmode['Time'] = 10
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('OFF')
            ATS.setEloadOnOff('ON')
            ATS.setEloadShort('ON')

            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.setDCPowerCurr(self.u_wkmode['Iin'])
            ATS.myScope.set_channel_autoscale(1, "ON", "DC",
                                              self.u_wkmode['Vin'], -3, 10)
            ATS.myScope.set_channel_autoscale(1, "ON", "DC",
                                              self.u_wkmode['Vout'], -3, 10)
            ATS.myScope.set_measure_clear()
            ATS.myScope.add_measure(2, "POV")
            ATS.myScope.add_measure(2, "MAX")
            ATS.myScope.set_resolution(100000)
            ATS.myScope.set_run()

        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        pass

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            if mode == 0:
                st_clk = clock()
                i = 0
                ATS.myScope.set_run()
                ATS.myScope.set_timebase(0.02, 10)
                ATS.myScope.set_trigger(1, "NORM", "RIS", 1)
                sleep(2)
                ATS.setDCPowerOnOff('ON')
                while clock() - st_clk < self.u_wkmode['Time'] + 2:
                    if clock() - st_clk > i:
                        i += 1
                        print('\u001b[0K' + "[process]" + "短路启动，预计" +
                              str(self.u_wkmode['Time'] + 3 - i) + "S后完成",
                              end='\r')
                        if i == 4:
                            if self.u_wkmode['Vin'] > 20:
                                scale = 10
                            else:
                                scale = 5
                            self.meas_out[2] = ATS.getScopeScreen(
                                self.u_wkmode['Path'] + '/Image', "-短路启动波形")
                            ATS.myScope.set_channel(1, "ON", "DC", scale, -3,
                                                    10)
                            ATS.myScope.set_timebase(0.02, 50)
                            ATS.myScope.set_trigger(
                                2, "NORM", "RIS", self.u_wkmode['Vout'] * 0.95)
                        if i == self.u_wkmode['Time']:
                            ATS.setEloadOnOff('OFF')
                            ATS.setEloadShort('OFF')
                ATS.myScope.set_stop()
                self.meas_out[3] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-短路启动恢复波形")
                sleep(1)
                float_tmp = ATS.myScope.get_measure_val(2, "POV")
                if float_tmp < 10000:
                    self.meas_out[1] = round(float_tmp, 3)
                float_tmp = ATS.myScope.get_measure_val(2, "MAX")
                if float_tmp < 10000:
                    self.meas_out[0] = round(float_tmp, 3)
                print("[process]" + "短路启动完成，等待后续测试")

            if mode == 1:
                st_clk = clock()
                i = 0
                ATS.myScope.set_channel(1, "ON", "DC", 5, -3, 10)
                ATS.myScope.set_run()
                ATS.myScope.set_timebase(0.02, 10)
                ATS.myScope.set_trigger(2, "NORM", "FALL",
                                        self.u_wkmode['Vout'] * 0.95)
                sleep(2)
                ATS.setEloadOnOff('ON')
                ATS.setEloadShort('ON')
                while clock() - st_clk < self.u_wkmode['Time'] + 2:
                    if clock() - st_clk > i:
                        i += 1
                        print('\u001b[0K' + '\u001b[0K' + "[process]" +
                              "运行短路，预计" + str(self.u_wkmode['Time'] + 3 - i) +
                              "S后完成",
                              end='\r')
                        if i == 4:
                            if self.u_wkmode['Vin'] > 20:
                                scale = 10
                            else:
                                scale = 5
                            self.meas_out[6] = ATS.getScopeScreen(
                                self.u_wkmode['Path'] + '/Image', "-运行短路波形")
                            ATS.myScope.set_channel(1, "ON", "DC", scale, -3,
                                                    10)
                            ATS.myScope.set_timebase(0.02, 50)
                            ATS.myScope.set_trigger(
                                2, "NORM", "RIS", self.u_wkmode['Vout'] * 0.95)
                        if i == self.u_wkmode['Time']:
                            ATS.setEloadOnOff('OFF')
                            ATS.setEloadShort('OFF')
                ATS.myScope.set_stop()
                self.meas_out[7] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-运行短路恢复波形")
                sleep(1)
                float_tmp = ATS.myScope.get_measure_val(2, "POV")
                if float_tmp < 10000:
                    self.meas_out[5] = round(float_tmp, 3)
                float_tmp = ATS.myScope.get_measure_val(2, "MAX")
                if float_tmp < 10000:
                    self.meas_out[4] = round(float_tmp, 3)
                print("[process]" + "运行短路完成，等待后续测试")

        except Exception as err:
            print("[process] set data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '电子负载', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    for i in range(3):
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
