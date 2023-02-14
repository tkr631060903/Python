# coding: utf-8
import sys
from corelib.autolib import ATS
from time import clock


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 4

        self.u_wkmode = {
            'Vin': 12,  # 直流电源电压设置
            'Iin': 5,
            'Vmax': 24,
            'Vdrop': 4.5,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V Vmax:" +
              str(self.u_wkmode['Vmax']) + "V 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('OFF')
            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.myDCPower.set_list({
                "index":
                0,
                "repeat":
                1,
                "points": [
                    "{0},2.45,0,10".format(self.u_wkmode['Vin']),
                    "{0},2.45,0,0.1".format(self.u_wkmode['Vmax']),
                    "{0},2.45,0,5".format(self.u_wkmode['Vin'])
                ]
            })
            ATS.myScope.set_resolution(100000)
            ATS.myScope.set_channel(1, "ON", "DC", 5, -3)
            ATS.myScope.set_channel(2, "ON", "DC", 1, -3)
            ATS.myScope.set_timebase(0.02, 20)
            ATS.myScope.set_trigger(
                1, "NORM", "RIS",
                (self.u_wkmode['Vin'] + self.u_wkmode['Vmax']) / 2)
            ATS.myScope.set_measure_clear()
            ATS.myScope.add_measure(1, "RIS")
            ATS.myScope.add_measure(1, "MAX")
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
            ATS.setDCPowerOnOff('ON')

            ATS.myDCPower.set_list_run([0])
            # ATS.setDCPowerOnOff('ON')
            ATS.myScope.set_run()
            i = 0
            stclk = clock()
            while clock() - stclk < 15:
                if clock() - stclk > i:
                    i += 1
                    print("[process]" + "当前电压:" +
                          str(round(self.u_wkmode['Vin'], 3)) + "V 预计" +
                          str(int(15 - i)) + "S后完成")
                    if i == 12:
                        ATS.myScope.set_stop()
            ATS.setDCPowerOnOff('OFF')
        except Exception as err:
            print("[process] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            self.meas_out[0] = ATS.getScopeScreen(
                self.u_wkmode['Path'] + '/Image', "-电源动态输入")
            float_tmp = ATS.myScope.get_measure_val(1, "RIS") * 1000000
            if float_tmp < 10000:
                self.meas_out[1] = round(float_tmp, 3)
            float_tmp = ATS.myScope.get_measure_val(1, "MAX")
            if float_tmp < 10000:
                self.meas_out[2] = round(float_tmp, 3)
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
