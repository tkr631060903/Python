#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.realpath("."))

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import json

from Material import Diode
from Material.Diode import Diode


class UIDataClass(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initValue()
        self.loadData()

    def initValue(self):
        #电阻变量初始化
        self.res_volUint = "V"
        self.res_freUint = "Hz"

        #电容变量初始化
        self.cap_volUint = "V"
        self.cap_freUint = "Hz"

        #电感变量初始化
        self.lnd_volUint = "V"
        self.lnd_freUint = "Hz"

        # 二极管变量初始化
        self.diode_volUint = "V"
        self.diode_currUint = "A"

        # 三极管变量初始化
        self.bjt_volUint = "V"
        self.bjt_currUint = "A"

        # 场效应管变量初始化
        self.mos_volUint = "V"
        self.mos_currUint = "A"

    def loadData(self):
        with open(r'D:\Data\Project\Python\ExcelATE_V2\Gui\UIData\Data.json', 'rb') as f:
            self.data = json.load(f)
        # 获取电阻数据
        self.res_testPurposeData = self.data.get("res_testPurpose")
        self.res_testInstrumentData = self.data.get("res_testInstrument")
        self.res_testStepData = self.data.get("res_testStep")

        # 获取电容数据
        self.cap_testPurposeData = self.data.get("cap_testPurpose")
        self.cap_testInstrumentData = self.data.get("cap_testInstrument")
        self.cap_testStepData = self.data.get("cap_testStep")

        # 获取电感数据
        self.lnd_testPurposeData = self.data.get("lnd_testPurpose")
        self.lnd_testInstrumentData = self.data.get("lnd_testInstrument")
        self.lnd_testStepData = self.data.get("lnd_testStep")

        # 获取二极管数据
        self.diode_testPurposeData = self.data.get("diode_testPurpose")
        self.diode_testInstrumentData = self.data.get("diode_testInstrument")
        self.diode_testStepData = self.data.get("diode_testStep")

        # 获取三极管数据
        self.bjt_testPurposeData = self.data.get("bjt_testPurpose")
        self.bjt_testInstrumentData = self.data.get("bjt_testInstrument")
        self.bjt_testStepData = self.data.get("bjt_testStep")

        # 获取场效应管数据
        self.mos_testPurposeData = self.data.get("mos_testPurpose")
        self.mos_testInstrumentData = self.data.get("mos_testInstrument")
        self.mos_testStepData = self.data.get("mos_testStep")


class TestThread(QThread):
    trigger = pyqtSignal()
    testStopTrigger = pyqtSignal()
    def __init__(self):
        super(TestThread, self).__init__()
        self.initValue()
        self.main = QMainWindow()
        Diode.testStopComplete = self.testStopComplete


    # 定义测试所需的所有参数(测试值,期望值,测试结果)
    def initValue(self):
        self.test_Mode = "Diode"
        self.test_VoltageValue = 0  # 测试电压
        self.test_CurrValue = 0  # 测试电流
        self.test_freValue = 0  # 测试频率
        self.diode_VoltageExpect = 0  # 二极管导通电压期望值
        self.diode_currExpect = 0  # 二极管漏电流期望值
        self.res_resExpect = 0  # 电阻阻抗期望值
        self.cap_capExpect = 0  # 电容容量期望值
        self.cap_esrExpect = 0  # 电容等效阻抗期望值
        self.lnd_lndExpect = 0  # 电感感量期望值
        self.lnd_qExpect = 0  # 电感品质因数
        self.bjt_VoltageExpect = 0  # 三极管导通电压期望值
        self.bjt_currExpect = 0  # 三极管集电极电流i-c期望值
        self.bjt_betaExpect = 0  # 三极管放大倍数期望值
        self.mos_VoltageExpect = 0  # 场效应管导通电压期望值
        self.mos_resExpect = 0  # 场效应管导通电阻期望值
        self.testStopComplete = False   # 测试停止状态

    # 开启测试线程
    def run(self):
        self.testStopComplete = False
        match self.test_Mode:
            case "Res":
                print("电阻测试")
            case "Cap":
                print("电容测试")
            case "Lnd":
                print("电感测试")
            case "Diode":
                Diode.testStopComplete = self.testStopComplete
                Diode.main(self,self.test_VoltageValue,self.test_CurrValue)
            case "Bjt":
                print("三极管测试")
            case "Mos":
                print("场效应管测试")
        if self.testStopComplete == False:
            self.trigger.emit()

    # 设置停止测试标志位
    def testStopQThread(self):
        self.testStopComplete = True
        Diode.testStopComplete = self.testStopComplete



if __name__ == "__main__":
    main = UIDataClass()


