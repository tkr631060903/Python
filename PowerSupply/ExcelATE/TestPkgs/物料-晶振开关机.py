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
            'Vin': 1.8,  # 直流电源电压设置
            'Iin': 0.5,  # 直流电源限流设置
            '序号': 1,
            'MHz': 27,
            'Volt': 1,
            'Time': 10,
            'Path': "E:/",
        }
        config = Config()
        self.do_cnt = 8
        ATS.getArgv(self.u_wkmode, sys.argv)
        self.cfg = config.getCfgMsg()
        self.msg = IMMsg(self.cfg)
        self.meas_out[0] = 0
        self.meas_out[1] = 0

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置

        # 初始化示波器
        ATS.myScope.set_measure_clear()
        ATS.myScope.add_measure(1, "FREQ")
        ATS.myScope.add_measure(1, "MAX")
        ATS.myScope.set_resolution(100000)
        ATS.myScope.set_timebase(0.0000004 / self.u_wkmode['MHz'], 30)

        # 初始化测试架
        do = [False] * 32
        ATS.myCraft.setChan(do)

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # 测试架测试通道设置
        do = [False] * 32
        index = (self.u_wkmode['序号'] - 1) % 14
        do[index] = [True]
        do[31] = [True]
        ATS.myCraft.setChan(do)
        ATS.setDCPowerOnOff('OFF')
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        ATS.setDCPowerOnOff('ON')
        ATS.myScope.set_run()
        sleep(0.2)

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            # 晶振起振频率：meas_out[0]；
            # 晶振开关机失败次数：meas_out[1]；
            # 晶振开关机测试次数：meas_out[2]；
            sum_out = 0
            ATS.myScope.set_stop()
            sleep(0.2)
            self.freq_out = ATS.myScope.get_measure_val(1, "FREQ")
            ATS.myScope.set_run()
            sleep(0.5)
            if self.freq_out < self.u_wkmode[
                    'MHz'] * 1.2 * 1000000 and self.freq_out > self.u_wkmode[
                        'MHz'] * 0.8 * 1000000:
                self.meas_out[0] = ATS.uint(self.freq_out)
                self.sum = 500 * self.u_wkmode['Time']
                for i in range(0, self.sum):
                    sum_out += 1
                    ATS.setDCPowerOnOff('ON')
                    sleep(0.2)
                    ATS.myScope.set_stop()
                    sleep(0.1)
                    freq = ATS.myScope.get_measure_val(1, "FREQ")
                    amp = ATS.myScope.get_measure_val(1, "MAX")
                    if freq > self.u_wkmode[
                            'MHz'] * 1.2 * 1000000 or freq < self.u_wkmode[
                                'MHz'] * 0.8 * 1000000 or amp < self.u_wkmode[
                                    'Vin'] * 0.3:
                        image = self.u_wkmode[
                            'Path'] + '/Image/' + ATS.getScopeScreen(
                                self.u_wkmode['Path'] + '/Image', "-异常波形")
                        freq = ATS.myScope.get_measure_val(1, "FREQ")
                        amp = ATS.myScope.get_measure_val(1, "MAX")
                        if freq > self.u_wkmode[
                                'MHz'] * 1.2 * 1000000 or freq < self.u_wkmode[
                                    'MHz'] * 0.8 * 1000000 or amp < self.u_wkmode[
                                        'Vin'] * 0.3:
                            self.meas_out[1] += 1
                            msg = {
                                "action":
                                "异常",
                                "msg": [
                                    image, "[" + str(self.u_wkmode['序号']) +
                                    "#] 晶振测试,第" + str(i + 1) + "次测试异常波形"
                                ]
                            }
                            self.msg.send(msg)

                    if i % 100 == 99:
                        msg = {
                            "action":
                            "完成",
                            "msg":
                            "[" + str(self.u_wkmode['序号']) + "#] 晶振测试：已完成" +
                            str(i + 1) + "次测试，失败" + str(self.meas_out[1]) +
                            "次."
                        }
                        self.msg.send(msg)

                    print('\u001b[0K' + "[process]" + "第" +
                          str(self.u_wkmode['序号']) + "组测试，" + "第" +
                          str(i + 1) + "次测试，" + str(self.meas_out[1]) + "次异常",
                          end='\r')
                    ATS.myScope.set_run()
                    ATS.setDCPowerOnOff('OFF')
                    sleep(0.2)
            else:
                self.meas_out[0] = "ERR"

            self.meas_out[2] = sum_out

            # 测试完毕，初始化DC电源，测试架
            ATS.myCraft.setChan([False] * 32)
            ATS.setDCPowerOnOff('OFF')

        except Exception as err:
            print("[err] get status error:" + str(err))


if __name__ == "__main__":
    use_devices = ['示波器', "直流电源", 'CRAFT']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    # for i in range(100):
    #     ate.U_SetStatus(i)
    #     ate.U_GetDatas(i)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
