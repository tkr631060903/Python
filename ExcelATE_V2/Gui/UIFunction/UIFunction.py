#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtGui import QRegExpValidator

# import threading

sys.path.append(os.path.realpath("."))

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow

# import json

# import pyqtgraph.exporters as pe
# from qt_material import apply_stylesheet
# import time
from win32com.client import DispatchEx

from Gui.UIView.UIView import UIViewClass
from Instrument.VisaInfo import VisaInfo
from Gui.UIView.UIView import TestWindow


class UIFunctionClass(UIViewClass, QMainWindow):

    def __init__(self):
        super(UIFunctionClass, self).__init__()
        self.testWindow = TestWindow()
        # apply_stylesheet(app, theme = 'dark_teal.xml') # 美化主题
        self.initEvent()
        
        # self.testQThread.test_VoltageValue = 1

    def initEvent(self):
        # 菜单触发事件
        self.impRes.triggered.connect(self.testRes)
        self.impCap.triggered.connect(self.testCap)
        self.impLnd.triggered.connect(self.testLnd)
        self.impDiode.triggered.connect(self.testDiode)
        self.impBjt.triggered.connect(self.testBjt)
        self.impMos.triggered.connect(self.testMos)
        self.impMes.triggered.connect(self.aboutAutoTest)
        self.reportOutMenu.triggered.connect(self.reportOut)

        # 触发开始测试
        self.btn.clicked.connect(self.testStart)

        # 触发停止测试
        self.testWindow.stopTestBtn.clicked.connect(self.testStop)

        # 触发测试完成
        self.testQThread.trigger.connect(self.testComplete)

        # 默认测试模式配置(二极管)
        self.diode_volComboBox.activated[str].connect(self.diode_volChange)
        self.diode_volLen.textChanged[str].connect(self.testDiodeVol)
        self.diode_currComboBox.activated[str].connect(self.diode_currChange)
        self.diode_currLen.textChanged[str].connect(self.testDiodeCurr)

    # 开始测试函数
    def testStart(self):
        try:            
            reply = QMessageBox.question(self, '提示', '请确认是否进行测试',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if not reply == QMessageBox.Yes:
                self.statusBar().showMessage('取消测试')
            else:
                my_instrument = VisaInfo.getInstrumentNum()
                if my_instrument == None:
                    if self.testQThread.test_Mode == 'Res' or self.testQThread.test_Mode == 'Cap' or self.testQThread.test_Mode == 'Lnd':
                        QMessageBox.information(self, '提示', '请连接LCR电桥')
                        self.statusBar().showMessage("请连接LCR电桥")
                    elif self.testQThread.test_Mode == "Diode" or self.testQThread.test_Mode == "Bjt" or self.testQThread.test_Mode == "Mos":
                        QMessageBox.information(self, '提示', '请连接程控电源')
                        self.statusBar().showMessage("请连接程控电源")
                else:
                    # devType = my_instrument.query("*IDN?")[11:18]  #获取程控电源型号
                    # if not devType == "IT6722A":
                    #     QMessageBox.information(self, '提示', '请连接程控电源')
                    #     self.statusBar().showMessage("请连接程控电源")                        
                    # else:
                        self.statusBar().showMessage('正在测试')
                        self.testWindow.show()  # 开始测试提示弹窗
                        self.testQThread.start()    # 打开测试线程
                        self.setDisabled(True)  # 禁用所有控件
        except Exception as e:
            print(e)

    # 手动停止测试函数
    def testStop(self):
        self.testQThread.testStopQThread()  # 设置停止测试标志位
        self.testWindow.close()
        self.setEnabled(True)  # 启用用所有控件
        self.statusBar().showMessage('停止测试')
        QMessageBox.information(self, '提示', '已停止测试')
        self.testQThread.exit()  # 退出线程
        self.testQThread.wait()  # 等待线程执行完毕退出

    # 测试完成函数
    def testComplete(self):
        self.testWindow.close()
        self.setEnabled(True)  # 启用用所有控件
        self.statusBar().showMessage('完成测试')
        QMessageBox.information(self, '提示', '完成测试')

    # excel导出pdf
    def reportOut(self):
        match self.testQThread.test_Mode:
            case "Res":
                print("电阻测试")
            case "Cap":
                print("电容测试")
            case "Lnd":
                print("电感测试")
            case "Diode":
                excel_path = r"{}".format(os.path.abspath('二极管.xlsx'))
                pdf_path = r"{}".format(os.path.abspath('二极管'))
            case "Bjt":
                excel_path = r"{}".format(os.path.abspath('三极管.xlsx'))
                pdf_path = r"{}".format(os.path.abspath('三极管'))
            case "Mos":
                excel_path = r"{}".format(os.path.abspath('场效应管.xlsx'))
                pdf_path = r"{}".format(os.path.abspath('场效应管'))
        excelApp = DispatchEx("Excel.Application")
        excelApp.Visible = False
        excelApp.DisplayAlerts = 0
        books = excelApp.Workbooks.Open(excel_path, False)
        books.ExportAsFixedFormat(0, pdf_path)
        books.Close(False)
        excelApp.Quit()
        QMessageBox.information(self, '提示', '已完成报告导出')
        self.statusBar().showMessage("已完成报告导出")

    # 关于器件自动化测试
    def aboutAutoTest(self):
        QMessageBox.information(
            self, "提示", "此软件为器件自动化测试工具\n\n欢迎反馈新功能和漏洞\n\nVersion : V1.0")

    # 电阻测试
    def testRes(self):
        if self.testQThread.test_Mode == "Res":
            pass
        else:
            self.testResConfig()
        self.res_volUint = "V"
        self.res_volComboBox.activated[str].connect(self.res_volChange)
        self.res_volLen.textChanged.connect(self.testResVol)

        self.res_freComboBox.activated[str].connect(self.res_freChange)
        self.res_freLen.textChanged.connect(self.testResFre)

    # 电阻测试电压单位变更触发函数
    def res_volChange(self, Uint):
        self.res_volUint = Uint
        if Uint == "V":
            self.res_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-1]"), self))
        else:
            self.res_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 电阻测试电压参数变更触发函数
    def testResVol(self, Voltage):
        if self.res_volUint == "V":
            self.test_VoltageValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_VoltageValue = float(Voltage) / 1000

    # 电阻测试频率单位变更触发函数
    def res_freChange(self, Uint):
        self.res_freUint = Uint
        if Uint == "Hz":
            self.res_freLen.setMaxLength(3)
        else:
            self.res_freLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 电阻测试频率参数变更触发函数
    def testResFre(self, Voltage):
        if self.res_freUint == "kHz":
            self.test_freValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_freValue = float(Voltage) / 1000

    # 电容测试
    def testCap(self):
        if self.testQThread.test_Mode == "Cap":
            pass
        else:
            self.testCapConfig()
        self.cap_volUint = "V"
        self.cap_volComboBox.activated[str].connect(self.cap_volChange)
        self.cap_volLen.textChanged.connect(self.testCapVol)

        self.cap_freComboBox.activated[str].connect(self.cap_freChange)
        self.cap_freLen.textChanged.connect(self.testCapFre)

    # 电容测试电压单位变更触发函数
    def cap_volChange(self, Uint):
        self.cap_volUint = Uint
        if Uint == "V":
            self.cap_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-1]"), self))
        else:
            self.cap_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 电容测试电压参数变更触发函数
    def testCapVol(self, Voltage):
        if self.cap_volUint == "V":
            self.test_VoltageValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_VoltageValue = float(Voltage) / 1000

    # 电容测试频率单位变更触发函数
    def cap_freChange(self, Uint):
        self.cap_freUint = Uint
        if Uint == "Hz":
            self.cap_freLen.setMaxLength(3)
        else:
            self.cap_freLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 电容测试频率参数变更触发函数
    def testCapFre(self, Voltage):
        if self.cap_freUint == "kHz":
            self.test_freValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_freValue = float(Voltage) / 1000

    # 电感测试
    def testLnd(self):
        if self.testQThread.test_Mode == "Lnd":
            pass
        else:
            self.testLndConfig()
        self.lnd_volUint = "V"
        self.lnd_volComboBox.activated[str].connect(self.lnd_volChange)
        self.lnd_volLen.textChanged.connect(self.testLndVol)

        self.lnd_freComboBox.activated[str].connect(self.lnd_freChange)
        self.lnd_freLen.textChanged.connect(self.testLndFre)

    # 电感测试电压单位变更触发函数
    def lnd_volChange(self, Uint):
        self.lnd_volUint = Uint
        if Uint == "V":
            self.lnd_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-1]"), self))
        else:
            self.lnd_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 电感测试电压参数变更触发函数
    def testLndVol(self, Voltage):
        if self.lnd_volUint == "V":
            self.test_VoltageValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_VoltageValue = float(Voltage) / 1000

    # 电感测试频率单位变更触发函数
    def lnd_freChange(self, Uint):
        self.lnd_freUint = Uint
        if Uint == "Hz":
            self.lnd_freLen.setMaxLength(3)
        else:
            self.lnd_freLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 电感测试频率参数变更触发函数
    def testLndFre(self, Voltage):
        if self.lnd_freUint == "kHz":
            self.test_freValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_freValue = float(Voltage) / 1000

    # 二极管测试
    def testDiode(self):
        if self.testQThread.test_Mode == "Diode":
            pass
        else:
            self.testDiodeConfig()
        self.diode_volUint = "V"
        self.diode_volComboBox.activated[str].connect(self.diode_volChange)
        self.diode_volLen.textChanged[str].connect(self.testDiodeVol)

        self.diode_currUint = "A"
        self.diode_currComboBox.activated[str].connect(self.diode_currChange)
        self.diode_currLen.textChanged[str].connect(self.testDiodeCurr)

    # 二极管测试电压单位变更触发函数
    def diode_volChange(self, Uint):
        self.diode_volUint = Uint
        if Uint == "V":
            print(Uint)
            self.diode_volLen.setValidator(
                QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"),
                                 self))
        else:
            print(Uint)
            self.diode_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 二极管测试电压参数变更触发函数
    def testDiodeVol(self, Voltage):
        if self.diode_volUint == "V":
            self.testQThread.test_VoltageValue = Voltage
        else:
            if Voltage.isdigit():
                self.testQThread.test_VoltageValue = float(Voltage) / 1000

    # 二极管测试电流单位变更触发函数
    def diode_currChange(self, Uint):
        self.diode_currUint = Uint
        if Uint == "A":
            self.diode_currLen.setValidator(
                QRegExpValidator(QRegExp("[0-9]|10"), self))
        else:
            self.diode_currLen.setValidator(
                QRegExpValidator(QRegExp("\d{3}"), self))

    # 二极管测试电流参数变更触发函数
    def testDiodeCurr(self, Current):
        if self.diode_currUint == "A":
            self.testQThread.test_CurrValue = Current
        else:
            if Current.isdigit():
                self.test_CurrValue = float(Current) / 1000

    # 三极管测试
    def testBjt(self):
        if self.testQThread.test_Mode == "Bjt":
            pass
        else:
            self.testBjtConfig()
        self.bjt_volUint = "V"
        self.bjt_volComboBox.activated[str].connect(self.bjt_volChange)
        self.bjt_volLen.textChanged[str].connect(self.testBjtVol)

        self.bjt_currUint = "A"
        self.bjt_currComboBox.activated[str].connect(self.bjt_currChange)
        self.bjt_currLen.textChanged[str].connect(self.testBjtCurr)

    # 三极管测试电压单位变更触发函数
    def bjt_volChange(self, Uint):
        self.bjt_volUint = Uint
        if Uint == "V":
            self.bjt_volLen.setValidator(
                QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"),
                                 self))
        else:
            self.bjt_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 三极管测试电压参数变更触发函数
    def testBjtVol(self, Voltage):
        if self.bjt_volUint == "V":
            self.test_VoltageValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_VoltageValue = float(Voltage) / 1000

    # 三极管测试电流单位变更触发函数
    def bjt_currChange(self, Uint):
        self.bjt_currUint = Uint
        if Uint == "A":
            self.bjt_currLen.setValidator(
                QRegExpValidator(QRegExp("[0-9]|10"), self))
        else:
            self.bjt_currLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 三极管测试电流参数变更触发函数
    def testBjtCurr(self, Current):
        self.test_CurrValue = Current
        if self.bjt_currUint == "A":
            self.test_CurrValue = Current
        else:
            if Current.isdigit():
                self.test_CurrValue = float(Current) / 1000

    # 场效应管测试
    def testMos(self):
        if self.testQThread.test_Mode == "Mos":
            pass
        else:
            self.testMosConfig()
        self.mos_volUint = "V"
        self.mos_volComboBox.activated[str].connect(self.mos_volChange)
        self.mos_volLen.textChanged[str].connect(self.testMosVol)

        self.mos_currUint = "A"
        self.mos_currComboBox.activated[str].connect(self.mos_currChange)
        self.mos_currLen.textChanged[str].connect(self.testMosCurr)

    # 场效应管测试电压单位变更触发函数
    def mos_volChange(self, Uint):
        self.mos_volUint = Uint
        if Uint == "V":
            self.mos_volLen.setValidator(
                QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"),
                                 self))
        else:
            self.mos_volLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 场效应管测试电压参数变更触发函数
    def testMosVol(self, Voltage):
        if self.mos_volUint == "V":
            self.test_VoltageValue = Voltage
        else:
            if Voltage.isdigit():
                self.test_VoltageValue = float(Voltage) / 1000

    # 场效应管测试电流单位变更触发函数
    def mos_currChange(self, Uint):
        self.mos_currUint = Uint
        if Uint == "A":
            self.mos_currLen.setValidator(
                QRegExpValidator(QRegExp("[0-9]|10"), self))
        else:
            self.mos_currLen.setValidator(
                QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))

    # 场效应管测试电流参数变更触发函数
    def testMosCurr(self, Current):
        self.test_CurrValue = Current
        if self.mos_currUint == "A":
            self.test_CurrValue = Current
        else:
            if Current.isdigit():
                self.test_CurrValue = float(Current) / 1000


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = UIFunctionClass()

    sys.exit(app.exec_())
