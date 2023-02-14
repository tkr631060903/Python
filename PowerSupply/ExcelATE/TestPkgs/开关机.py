# coding: utf-8
import sys
from corelib.autolib import ATS
import os
from os import path
from time import clock
from datetime import datetime

from corelib.config import Config
# from corelib.immsg import IMMsg

class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""] * 11
        self.u_wkmode = {
            'Vin': 24,  # 直流电源电压设置
            'Iin': 3,
            '超时': 10,
            '间隔': 3,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        config = Config()
        self.serial = config.getCfgSerial()
        self.run = True
        self.st_clk = clock()
        self.cfg = config.getCfgMsg()
        # self.msg = IMMsg(self.cfg)
        ATS.getArgv(self.u_wkmode, sys.argv)

        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 测试中")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        self.meas_out[0] = "0"
        print(str(self.serial))
        ATS.setDCPowerOnOff('OFF')
        ATS.setDCPowerVolt(self.u_wkmode['Vin'])
        ATS.setDCPowerCurr(self.u_wkmode['Iin'])
        print("[log clr]")

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        try:
            ATS.setDCPowerOnOff('OFF')
            for item in self.serial:
                item["log_aux"] = ""
                item["log"] = ""
                item["result"] = ""
                if item["ser"].isOpen():
                    item["ser"].read_all()
                if item["ser_aux"] is not None:
                    item["ser_aux"].read_all()
            st_clk = clock()
            i = 0
            while clock() - st_clk < self.u_wkmode['间隔']:
                if clock() - st_clk > i:
                    i += 1
                    print('\u001b[0K' + "[process]" + "第" + str(mode + 1) +
                          "次测试，预计" + str(int(self.u_wkmode['间隔'] + 1 - i)) +
                          "S后启动",
                          end='\r')
            ATS.setDCPowerOnOff('ON')
            print("[log clr]")
        except Exception as err:
            print("[err] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            st_clk = clock()
            i = 0
            sucess = 0
            str_tmp = ""
            while clock() - st_clk < self.u_wkmode['超时'] and sucess < len(
                    self.serial):
                if clock() - st_clk > i:
                    i += 1
                    str_total = ""
                    for item in self.serial:
                        if item["ser"].isOpen():
                            try:
                                str_tmp = item["ser"].read_all().decode(
                                    'utf-8')
                            except Exception:
                                pass
                            # if item["id"] == 0:
                            if len(str_tmp) > 1:
                                str_print = "[log@" + str(
                                    item["id"]) + "]" + str_tmp.replace(
                                        "\r",
                                        "\r[log@" + str(item["id"]) + "]")
                                print(str_print)
                                item["log"] += str_tmp
                            str_total += " "+item["note"] + \
                                " R:"+str(len(item["log"]))
                            if item["key"] is not None:
                                if item["result"] != "success":
                                    if item["log"].find(item["key"]) > 0:
                                        print("[process]" + "第" +
                                              str(mode + 1) + "次测试，" +
                                              item["note"] + str(i) + "S启动成功",
                                              end='\r')
                                        item["result"] = "success"
                                        sucess += 1
                            if item["key_err"] is not None:
                                if item["result"] != "error":
                                    if item["log"].find(item["key_err"]) > 0:
                                        print("[process]" + "检测到错误关键字")
                                        item["result"] = "error"
                        if item["ser_aux"] is not None:
                            try:
                                item["log_aux"] += item["ser_aux"].read_all(
                                ).decode('utf-8')
                            except Exception:
                                pass

                    print('\u001b[0K' + "[process]" + "第" + str(mode + 1) +
                          "次测试，预计" + str(int(self.u_wkmode['超时'] + 1 - i)) +
                          "S后重启" + str_total,
                          end='\r')
            i = 0
            msg = {"action": "", "msg": ""}
            for item in self.serial:
                if item["result"] != "success":
                    filename = path.join(
                        self.u_wkmode['Path'], "Log", '{0}错误日志.txt'.format(
                            datetime.now().strftime('%Y%m%d-%H%M%S-') +
                            item["note"]))
                    # wb means open for writing in binary; can overwrite
                    logfile = open(filename, "w")
                    # print(str(gsfile))
                    logfile.write(item["log"])
                    logfile.close()
                    if item["ser_aux"] is not None:
                        filename = path.join(
                            self.u_wkmode['Path'], "Log",
                            '{0}辅助串口错误日志.txt'.format(
                                datetime.now().strftime('%Y%m%d-%H%M%S-') +
                                item["note"]))
                        # wb means open for writing in binary; can overwrite
                        logfile = open(filename, "w")
                        # print(str(gsfile))
                        logfile.write(item["log_aux"])
                        logfile.close()

                    item["err_cnt"] += 1
                    if msg["action"] == "":
                        msg["action"] = "异常"
                    msg["msg"] += item["note"] + "未正常启动\n"
                if item["result"] == "error":
                    msg["action"] = "终止"
                    msg["msg"] += item["note"] + "检测到错误关键字" + item[
                        "key_err"] + "\n"
                self.meas_out[i] = str(item["err_cnt"])
                i += 1
            if msg["action"] != "":
                msg["msg"] = str(self.u_wkmode["Vin"]) + "V开关机 第" + str(
                    mode + 1) + "次测试" + msg["action"] + "!\n" + msg["msg"]
                self.msg.send(msg)
            if msg["action"] == "终止":
                os._exit(0)
        except Exception as err:
            print("[err] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    num = 100
    for i in range(num):
        ate.U_SetStatus(i)
        ate.U_GetDatas(i)
    str_temp = ""
    for item in ate.serial:
        if item["err_cnt"] > 0:
            str_temp += item["note"] + "失败" + str(item["err_cnt"]) + "次\n"
        else:
            str_temp += item["note"] + "全部启动成功\n"
    msg = {
        "action": "完成",
        "msg":
        str(ate.u_wkmode['Vin']) + "V 开关机" + str(num) + "次测试完成\n" + str_temp
    }
    ate.msg.send(msg)
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
