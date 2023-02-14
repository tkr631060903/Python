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
        self.meas_out = [""] * 11
        self.u_wkmode = {
            'Vin': 12,  # 直流电源电压设置
            'Iin': 2,
            'Ioh': 3,
            'Iol': 0.3,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V Iol:" +
              str(self.u_wkmode['Iol']) + "A Ioh:" +
              str(self.u_wkmode['Ioh']) + "A 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('ON')
            ATS.setEloadOnOff('ON')

            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.setDCPowerCurr(self.u_wkmode['Iin'])

            ATS.myScope.set_channel(1, "ON", "DC", 1, -3, 10, "A")
            ATS.myScope.set_channel(2, "ON", "AC", 0.5, 3, 10)
            ATS.myScope.set_timebase(0.0005, 40)
            ATS.myScope.set_trigger(
                1, "NORM", "RIS",
                (self.u_wkmode['Ioh'] + self.u_wkmode['Iol']) * 0.5)
            ATS.myScope.set_measure_clear()
            ATS.myScope.add_measure(2, "MAX")
            ATS.myScope.add_measure(2, "MINI")
            ATS.myScope.set_resolution(100000)
            ATS.myEload.set_dynamic("CONT", self.u_wkmode['Ioh'], 0.001,
                                    self.u_wkmode['Iol'], 0.002)
            ATS.myScope.set_run()

        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 设置其他工作条件，如改变设备状态，加入延时等等
        # ATS.setNI9472DO('0:5', [True] + [False]*4 + [True])
        pass

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            st_clk = clock()
            i = 0
            while clock() - st_clk < 5:
                if clock() - st_clk > i:
                    i += 1
                    print(
                        '\u001b[0K' + "[process]" + "@输入电压:" + str(
                            self.u_wkmode['Vin']) + "V Iol:" + str(
                                self.u_wkmode['Iol']) + "A Ioh:" + str(
                                    self.u_wkmode['Ioh']) + "A 预计" + str(8 - i)
                        + "S后完成",
                        end='\r')
                    if i == 3:
                        ATS.myScope.set_stop()
            float_tmp = ATS.myScope.get_measure_val(2, "MAX") * 1000.0
            if float_tmp < 10000:
                self.meas_out[0] = round(float_tmp, 3)
            float_tmp = ATS.myScope.get_measure_val(2, "MINI") * 1000.0
            if float_tmp < 10000:
                self.meas_out[1] = round(float_tmp, 3)
            self.meas_out[2] = ATS.getScopeScreen(
                self.u_wkmode['Path'] + '/Image', "-波形")
            ATS.setEloadCCval(0)
        except Exception as err:
            print("[process] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '电子负载', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
