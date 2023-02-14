# coding: utf-8
import sys
from corelib.autolib import ATS
from time import sleep

u_time_scale = 50.0  # 示波器 Horizontal ms/div
u_time_noise_scale = 10.0  # 示波器测噪声时 Horizontal us/div


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
            'Iout': 0,
            'Path': "E:/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 负载电流:" +
              str(self.u_wkmode['Iout']) + "A 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('OFF')
            ATS.setEloadOnOff('ON')
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
                ATS.setDCPowerVolt(self.u_wkmode['Vin'])
                ATS.setDCPowerCurr(self.u_wkmode['Iin'])
                ATS.setEloadCCval(self.u_wkmode['Iout'])
                if self.u_wkmode['Vin'] > 20:
                    scale = 10
                else:
                    scale = 5
                ATS.myScope.set_channel(1, "ON", "DC", scale, -2, 10)
                ATS.myScope.set_channel(2, "ON", "DC", 2, -2, 10)
                ATS.myScope.set_timebase(u_time_scale / 1000.0, 30)
                ATS.myScope.set_trigger(1, "NORM", "RIS",
                                        self.u_wkmode['Vin'] / 2)
                ATS.myScope.set_measure_clear()
                ATS.myScope.add_measure(2, "POV")
                ATS.myScope.add_measure(2, "RIS")
                ATS.myScope.set_resolution(100000)

                ATS.myScope.set_run()
                sleep(2)
                ATS.setDCPowerOnOff('ON')
                sleep(2)
                ATS.myScope.set_stop()

            except Exception as err:
                print("[process] set status error:" + str(err))
        elif mode == 1:  # 运行测试
            try:
                ATS.myScope.set_measure_clear()
                ATS.myScope.add_measure(2, "AMP")
                ATS.myScope.set_channel(2, "ON", "AC", 0.2, 0, 10)
                ATS.myScope.set_trigger(2, "AUTO")
                ATS.myScope.set_timebase(u_time_noise_scale / 1000000.0, 50)
                ATS.myScope.set_run()
                sleep(5)
                ATS.myScope.set_stop()

            except Exception as err:
                print("[process] set status error:" + str(err))

        elif mode == 2:  # 关机测试
            try:
                ATS.myScope.set_measure_clear()
                # ATS.myScope.set_measure_all()
                ATS.myScope.add_measure(2, "FALL")
                if self.u_wkmode['Vin'] > 20:
                    scale = 10
                else:
                    scale = 5
                ATS.myScope.set_channel(2, "ON", "DC", 2, -2, 10)
                ATS.myScope.set_timebase(u_time_scale / 1000.0, 60)
                ATS.myScope.set_trigger(1, "NORM", "FALL",
                                        self.u_wkmode['Vin'] / 2)
                ATS.myScope.set_run()
                sleep(1)
                ATS.setDCPowerOnOff('OFF')
                sleep(2)
                ATS.myScope.set_stop()
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
                self.meas_out[8] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-启动波形")
                float_tmp = ATS.myScope.get_measure_val(2, "RIS") * 1000.0
                if float_tmp < 10000:
                    self.meas_out[6] = round(float_tmp, 3)
                float_tmp = ATS.myScope.get_measure_val(2, "POV")
                if float_tmp < 100.0:
                    self.meas_out[5] = round(float_tmp, 3)
            elif mode == 1:  # 运行测试
                self.meas_out[9] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-运行波形")
                self.meas_out[0] = round(ATS.getDCPowerMeasVolt(), 3)
                self.meas_out[1] = round(ATS.getDCPowerMeasCurr(), 3)
                self.meas_out[2] = round(ATS.getEloadMeasVolt(), 3)
                self.meas_out[3] = round(ATS.getEloadMeasCurr(), 3)
                float_tmp = ATS.myScope.get_measure_val(2, "AMP") * 1000.0
                if float_tmp < 10000:
                    self.meas_out[4] = round(float_tmp, 3)
            elif mode == 2:  # 关机测试
                self.meas_out[10] = ATS.getScopeScreen(
                    self.u_wkmode['Path'] + '/Image', "-关机波形")
                float_tmp = ATS.myScope.get_measure_val(2, 'FALL') * 1000.0
                if float_tmp < 10000:
                    self.meas_out[7] = round(float_tmp, 3)

            pass
        except Exception as err:
            print("[process] get data error:" + str(err))


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
