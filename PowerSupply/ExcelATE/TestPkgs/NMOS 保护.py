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
            'Vin': 12,  # 直流电源电压设置
            'Iin': 2,
            'Iout': 0,
            'Path': "E:/Workspace/Software/ExcelATE",
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
        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 设置其他工作条件，如改变设备状态，加入延时等等
        # ATS.setNI9472DO('0:5', [True] + [False]*4 + [True])
        try:
            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.setDCPowerCurr(self.u_wkmode['Iin'])
            ATS.setDCPowerOnOff('ON')

            if self.u_wkmode['Vin'] > 20:
                scale = 10
            else:
                scale = 5
            # 通道设置
            ATS.myScope.set_channel(1, "ON", "DC", 10, 2, 10)
            ATS.myScope.set_channel(2, "ON", "DC", 10, 0, 10)
            ATS.myScope.set_channel(3, "ON", "DC", 20, -2, 10)
            ATS.myScope.set_channel(4, "ON", "DC", 10, -4, 10)

            # ATS.myScope.set_timebase(u_time_scale / 1000.0, 30)
            # ATS.myScope.set_trigger(1, "NORM", "RIS",
            #                         self.u_wkmode['Vin'] / 2)
            ATS.myScope.set_measure_clear()
            ATS.myScope.add_measure(1, "MAXI")
            ATS.myScope.add_measure(2, "MAXI")
            ATS.myScope.add_measure(3, "MAXI")
            ATS.myScope.add_measure(4, "MAXI")
            ATS.myScope.set_resolution(100000)

            ATS.myScope.set_run()
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
            float_tmp = ATS.myScope.get_measure_val(1, "MAXI")
            # if float_tmp < 100.0:
            self.meas_out[0] = round(float_tmp, 3)
            float_tmp = ATS.myScope.get_measure_val(1, "MAXI")
            if float_tmp < 100.0:
                self.meas_out[1] = round(float_tmp, 3)
            float_tmp = ATS.myScope.get_measure_val(1, "MAXI")
            if float_tmp < 100.0:
                self.meas_out[2] = round(float_tmp, 3)
            float_tmp = ATS.myScope.get_measure_val(1, "MAXI")
            if float_tmp < 100.0:
                self.meas_out[3] = round(float_tmp, 3)
            self.meas_out[4] = ATS.getScopeScreen(
            self.u_wkmode['Path'] + '/Image', "-波形")
        except Exception as err:
            print("[process] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
