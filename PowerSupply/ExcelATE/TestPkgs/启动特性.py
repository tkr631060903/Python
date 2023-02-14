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
        self.meas_out = [""] * 4

        self.u_wkmode = {
            'Vin': 24,  # 直流电源电压设置
            'Iin': 5,
            '超时': 10,
            'Type': 1,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        self.tim = 1
        ATS.getArgv(self.u_wkmode, sys.argv)

        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) +
              "V 测试波形 TYPE:" + str(self.u_wkmode['Type']) + " 测试中")

    def getWave(self, _un, _type):
        if _type < 4:
            if _un == 12:
                start = 1 + (_type - 1) * 3
            else:
                start = 11 + (_type - 1) * 3
            return [start, start + 1, start + 2]
        elif _type == 4:
            if _un == 12:
                return [0, 5, 10]

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置22
        try:
            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.myScope.set_resolution(100000)
            # ATS.myScope.set_channel(2, "ON", "DC", 1, -3)
            # ATS.myScope.set_timebase(0.2, 5)
            # ATS.myScope.set_trigger(1, "NORM", "FALL",
            #                         self.u_wkmode['Vin'] - 2)
            # ATS.myScope.set_measure_clear()
            # ATS.myScope.add_measure(1, "FALL")
            # ATS.myScope.add_measure(1, "MINI")
            # ATS.myScope.add_measure(2, "MINI")
            # ATS.myScope.set_run()
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
            # ATS.myScope.set_run()
            ATS.setDCPowerOnOff('OFF')
            sleep(1)
            ATS.setDCPowerOnOff('ON')
            ATS.myDCPower.set_list_run(
                self.getWave(self.u_wkmode['Vin'], self.u_wkmode['Type']))

            i = 0
            stclk = clock()
            while clock() - stclk < self.u_wkmode['超时']:
                if clock() - stclk > i:
                    i += 1
                    print(
                        '\u001b[0K' + "[process]" + "第" +
                        str(mode + 1) + "次测试，预计" + str(
                            int(self.u_wkmode['超时'] + 1 - i)) + "S后完成",
                        end='\r')
            # ATS.myScope.set_stop()
            # ATS.setDCPowerOnOff('OFF')
        except Exception as err:
            print("[process] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            pass
            # self.meas_out[0] = ATS.getScopeScreen(
            #     self.u_wkmode['Path'] + '/Image', "-电压瞬间下降")
            # float_tmp = ATS.myScope.get_measure_val(1, "FALL") * 1000
            # if float_tmp < 10000:
            #     self.meas_out[1] = round(float_tmp, 3)
            # float_tmp = ATS.myScope.get_measure_val(1, "MINI")
            # if float_tmp < 10000:
            #     self.meas_out[2] = round(float_tmp, 3)
            # float_tmp = ATS.myScope.get_measure_val(2, "MINI")
            # if float_tmp < 10000:
            #     self.meas_out[3] = round(float_tmp, 3)
        except Exception as err:
            print("[process] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源', '示波器']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    for i in range(10):
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
