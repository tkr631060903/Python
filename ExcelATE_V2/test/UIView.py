#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.realpath("."))

from PyQt5.QtWidgets import * # QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu, QInputDialog, QLineEdit, QLabel, QComboBox
from PyQt5.QtGui import * # QFont, QDoubleValidator, QIcon
from PyQt5.QtCore import * # QCoreApplication

from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np
import pyqtgraph.exporters as pe
import qdarkstyle, requests, time, random, json, datetime, re
from qt_material import apply_stylesheet

from Gui.UIData.UIData import UIDataClass
from Gui.UIData.UIData import TestThread


class UIViewClass(UIDataClass, QMainWindow):

    def __init__(self):
        super().__init__()
        self.testQThread = TestThread()
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # 美化风格
        # apply_stylesheet(app, theme = 'dark_teal.xml')    # 美化风格
        self.initUI()

    def initUI(self):
        self.testInitConfig()
        # 状态栏信息
        self.statusBar().showMessage('请设定测试参数')

        # 配置一级菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        testMenu = menubar.addMenu('测试模式')
        messageMenu = menubar.addMenu('信息')

        # 配置文件菜单
        self.impIn = QAction('导入测试模板', self)
        self.impOut = QAction('导出测试数据', self)
        fileMenu.addAction(self.impIn)
        fileMenu.addAction(self.impOut)

        # 配置测试菜单
        self.impRes = QAction('电阻测试', self)
        self.impCap = QAction('电容测试', self)
        self.impLnd = QAction('电感测试', self)
        self.impDiode = QAction('二极管测试', self)
        self.impBjt = QAction('三极管测试', self)
        self.impMos = QAction('场效应管测试', self)
        testMenu.addAction(self.impRes)
        testMenu.addAction(self.impCap)
        testMenu.addAction(self.impLnd)
        testMenu.addAction(self.impDiode)
        testMenu.addAction(self.impBjt)
        testMenu.addAction(self.impMos)

        # 配置信息菜单
        self.impMes = QAction("关于器件自动化测试工具",self)
        messageMenu.addAction(self.impMes)

        # 配置主窗口布局
        self.mainWidget()

        # 开始按钮
        self.btn = QPushButton('开始测试', self)
        self.btn.setToolTip('点击开始器件测试')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(750, 500)

        # 退出按钮
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(890, 500)


        # 窗口和标题并创建所有控件
        self.setGeometry(580, 270, 1024, 576)
        self.center()
        self.setWindowTitle('器件自动化测试')
        self.setWindowIcon(QIcon('Gui/UIView/favicon.ico'))
        self.setFixedSize(self.width(), self.height())  # 固定窗口大小和关闭最大化
        self.show()

        self.res_QGroupBox.close()
        self.res_explainQGroupBox.close()
        self.cap_QGroupBox.close()
        self.cap_explainQGroupBox.close()
        self.lnd_QGroupBox.close()
        self.lnd_explainQGroupBox.close()
        self.bjt_QGroupBox.close()
        self.bjt_explainQGroupBox.close()
        self.mos_QGroupBox.close()
        self.mos_explainQGroupBox.close()

    # 配置主窗口布局
    def mainWidget(self):
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.res_QGroupBox,1,0)
        mainLayout.addWidget(self.res_resultQGroupBox,1,1)
        mainLayout.addWidget(self.res_explainQGroupBox,2,0,1,2)

        mainLayout.addWidget(self.cap_QGroupBox,1,0)
        mainLayout.addWidget(self.cap_resultQGroupBox,1,1)
        mainLayout.addWidget(self.cap_explainQGroupBox,2,0,1,2)

        mainLayout.addWidget(self.lnd_QGroupBox,1,0)
        mainLayout.addWidget(self.lnd_resultQGroupBox,1,1)
        mainLayout.addWidget(self.lnd_explainQGroupBox,2,0,1,2)

        mainLayout.addWidget(self.diode_QGroupBox,1,0)
        mainLayout.addWidget(self.diode_resultQGroupBox,1,1)
        mainLayout.addWidget(self.diode_explainQGroupBox,2,0,1,2)

        mainLayout.addWidget(self.bjt_QGroupBox,1,0)
        mainLayout.addWidget(self.bjt_resultQGroupBox,1,1)
        mainLayout.addWidget(self.bjt_explainQGroupBox,2,0,1,2)

        mainLayout.addWidget(self.mos_QGroupBox,1,0)
        mainLayout.addWidget(self.mos_resultQGroupBox,1,1)
        mainLayout.addWidget(self.mos_explainQGroupBox,2,0,1,2)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)

    # 窗口居中
    def center(self):
        qr = self.frameGeometry()  # 获得主窗口所在的框架
        cp = QDesktopWidget().availableGeometry().center()  # 获取显示器的分辨率，然后得到屏幕中间点的位置
        qr.moveCenter(cp)  # 然后把主窗口框架的中心点放置到屏幕的中心位置
        self.move(qr.topLeft())  # 然后通过move函数把主窗口的左上角移动到其框架的左上角，这样就把窗口居中了

    # 关闭窗口提示
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '确认是否退出',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 初始化所有UI测试项目
    def testInitConfig(self):
        self.res_testInitConfig()
        self.cap_testInitConfig()
        self.lnd_testInitConfig()
        self.bjt_testInitConfig()
        self.mos_testInitConfig()
        self.diode_testInitConfig()

        # 测试结果
        self.ins_resultLab = QLabel("测试结果0：", self)
        self.ins_resultLab.setGeometry(560, 100, 200, 40)
        self.ins_resultLab1 = QLabel("测试结果1：", self)
        self.ins_resultLab1.setGeometry(560, 150, 200, 40)
        self.ins_resultLab2 = QLabel("测试结果2：", self)
        self.ins_resultLab2.setGeometry(560, 200, 200, 40)
        self.ins_resultLab3 = QLabel("测试结果3：", self)
        self.ins_resultLab3.setGeometry(560, 250, 200, 40)

    # 电阻测试UI初始化
    def res_testInitConfig(self):
        self.res_QGroupBox = QGroupBox("测试参数")
        self.res_resultQGroupBox = QGroupBox("测试结果")
        self.res_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QGridLayout()
        explainLayout = QGridLayout()

        self.res_modeLab = QLabel("当前为电阻测试模式", self)

        self.res_volLab = QLabel('测试电压：', self)
        self.res_volLen = QLineEdit('请输入测试电压值', self)
        self.res_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),self)) # 按照正则表达式设定可输入的内容
        self.testQThread.test_VoltageValue = 1
        self.res_volLen.setText("{}".format(self.testQThread.test_VoltageValue))
        self.res_volComboBox = QComboBox(self)
        self.res_volComboBox.addItem("V")
        self.res_volComboBox.addItem("mV")

        self.res_freLab = QLabel('测试频率：', self)
        self.res_freLen = QLineEdit('请输入测试频率值', self)
        self.res_freLen.setMaxLength(3)
        self.testQThread.test_freValue = 100
        self.res_freLen.setText("{}".format(self.testQThread.test_freValue))
        self.res_freComboBox = QComboBox(self)
        self.res_freComboBox.addItem("Hz")
        self.res_freComboBox.addItem("kHz")

        self.res_resExpectLab = QLabel('电阻阻值：', self)
        self.res_resExpectLen = QLineEdit('请输入电阻阻值', self)
        self.res_resExpectLen.setMaxLength(3)
        self.testQThread.res_resExpect = 100
        self.res_resExpectLen.setText("{}".format(self.testQThread.res_resExpect))
        self.res_resExpectComboBox = QComboBox(self)
        self.res_resExpectComboBox.addItem("MΩ")
        self.res_resExpectComboBox.addItem("kΩ")
        self.res_resExpectComboBox.addItem("Ω")
        self.res_resExpectComboBox.addItem("mΩ")
        self.res_resExpectComboBox.setCurrentIndex(2) # 设置默认单位值

        self.res_testPurpose = QLabel(self.res_testPurposeData, self)
        self.res_testInstrument = QLabel(self.res_testInstrumentData, self)
        self.res_testStep = QLabel(self.res_testStepData, self)

        layout.addWidget(self.res_modeLab,1,0)
        layout.addWidget(self.res_volLab,2,0)
        layout.addWidget(self.res_volLen,2,1)
        layout.addWidget(self.res_volComboBox,2,2)
        layout.addWidget(self.res_freLab)
        layout.addWidget(self.res_freLen)
        layout.addWidget(self.res_freComboBox)
        layout.addWidget(self.res_resExpectLab)
        layout.addWidget(self.res_resExpectLen)
        layout.addWidget(self.res_resExpectComboBox)

        explainLayout.addWidget(self.res_testPurpose)
        explainLayout.addWidget(self.res_testInstrument)
        explainLayout.addWidget(self.res_testStep)

        self.res_QGroupBox.setLayout(layout)
        self.res_explainQGroupBox.setLayout(explainLayout)

    # 电容测试UI初始化
    def cap_testInitConfig(self):
        self.cap_QGroupBox = QGroupBox("测试参数")
        self.cap_resultQGroupBox = QGroupBox("测试结果")
        self.cap_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QGridLayout()
        explainLayout = QGridLayout()

        self.cap_modeLab = QLabel("当前为电容测试模式", self)

        self.cap_volLab = QLabel('测试电压：', self)
        self.cap_volLen = QLineEdit('请输入测试电压值', self)
        self.cap_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),self)) # 按照正则表达式设定可输入的内容
        self.testQThread.test_VoltageValue = 1
        self.cap_volLen.setText("{}".format(self.testQThread.test_VoltageValue))
        self.cap_volComboBox = QComboBox(self)
        self.cap_volComboBox.addItem("V")
        self.cap_volComboBox.addItem("mV")

        self.cap_freLab = QLabel('测试频率：', self)
        self.cap_freLen = QLineEdit('请输入测试频率值', self)
        self.cap_freLen.setMaxLength(3)
        self.testQThread.test_freValue = 100
        self.cap_freLen.setText("{}".format(self.testQThread.test_freValue))
        self.cap_freComboBox = QComboBox(self)
        self.cap_freComboBox.addItem("Hz")
        self.cap_freComboBox.addItem("kHz")

        self.cap_capExpectLab = QLabel('电容值：', self)
        self.cap_capExpectLen = QLineEdit('请输入电容值', self)
        self.cap_capExpectLen.setMaxLength(3)
        self.testQThread.cap_capExpect = 100
        self.cap_capExpectLen.setText("{}".format(self.testQThread.cap_capExpect))
        self.cap_capExpectComboBox = QComboBox(self)
        self.cap_capExpectComboBox.addItem("F")
        self.cap_capExpectComboBox.addItem("mF")
        self.cap_capExpectComboBox.addItem("uF")
        self.cap_capExpectComboBox.addItem("nF")
        self.cap_capExpectComboBox.addItem("pF")
        self.cap_capExpectComboBox.setCurrentIndex(2)

        self.cap_esrExpectLab = QLabel('等效串联电阻：', self)
        self.cap_esrExpectLen = QLineEdit('请输入等效串联电阻值', self)
        self.cap_esrExpectLen.setMaxLength(3)
        self.testQThread.cap_esrExpect = 100
        self.cap_esrExpectLen.setText("{}".format(self.testQThread.cap_esrExpect))
        self.cap_esrExpectComboBox = QComboBox(self)
        self.cap_esrExpectComboBox.addItem("kΩ")
        self.cap_esrExpectComboBox.addItem("Ω")
        self.cap_esrExpectComboBox.addItem("mΩ")
        self.cap_esrExpectComboBox.setCurrentIndex(1)

        self.cap_testPurpose = QLabel(self.cap_testPurposeData, self)
        self.cap_testInstrument = QLabel(self.cap_testInstrumentData, self)
        self.cap_testStep = QLabel(self.cap_testStepData, self)

        layout.addWidget(self.cap_modeLab,1,0)
        layout.addWidget(self.cap_volLab,2,0)
        layout.addWidget(self.cap_volLen,2,1)
        layout.addWidget(self.cap_volComboBox,2,2)
        layout.addWidget(self.cap_freLab)
        layout.addWidget(self.cap_freLen)
        layout.addWidget(self.cap_freComboBox)
        layout.addWidget(self.cap_capExpectLab)
        layout.addWidget(self.cap_capExpectLen)
        layout.addWidget(self.cap_capExpectComboBox)
        layout.addWidget(self.cap_esrExpectLab)
        layout.addWidget(self.cap_esrExpectLen)
        layout.addWidget(self.cap_esrExpectComboBox)

        explainLayout.addWidget(self.cap_testPurpose)
        explainLayout.addWidget(self.cap_testInstrument)
        explainLayout.addWidget(self.cap_testStep)

        self.cap_QGroupBox.setLayout(layout)
        self.cap_explainQGroupBox.setLayout(explainLayout)

    # 电感测试UI初始化
    def lnd_testInitConfig(self):
        self.lnd_QGroupBox = QGroupBox("测试参数")
        self.lnd_resultQGroupBox = QGroupBox("测试结果")
        self.lnd_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QGridLayout()
        explainLayout = QGridLayout()

        self.lnd_modeLab = QLabel("当前为电感测试模式", self)

        self.lnd_volLab = QLabel('测试电压：', self)
        self.lnd_volLen = QLineEdit('请输入测试电压值', self)
        self.lnd_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),self)) # 按照正则表达式设定可输入的内容
        self.testQThread.test_VoltageValue = 1
        self.lnd_volLen.setText("{}".format(self.testQThread.test_VoltageValue))
        self.lnd_volComboBox = QComboBox(self)
        self.lnd_volComboBox.addItem("V")
        self.lnd_volComboBox.addItem("mV")

        self.lnd_freLab = QLabel('测试频率：', self)
        self.lnd_freLen = QLineEdit('请输入测试频率值', self)
        self.lnd_freLen.setMaxLength(3)
        self.testQThread.test_freValue = 100
        self.lnd_freLen.setText("{}".format(self.testQThread.test_freValue))
        self.lnd_freComboBox = QComboBox(self)
        self.lnd_freComboBox.addItem("Hz")
        self.lnd_freComboBox.addItem("kHz")

        self.lnd_lndExpectLab = QLabel('电感值：', self)
        self.lnd_lndExpectLen = QLineEdit('请输入电感值', self)
        self.lnd_lndExpectLen.setMaxLength(3)
        self.testQThread.lnd_lndExpect = 100
        self.lnd_lndExpectLen.setText("{}".format(
            self.testQThread.lnd_lndExpect))
        self.lnd_lndExpectComboBox = QComboBox(self)
        self.lnd_lndExpectComboBox.addItem("Hz")
        self.lnd_lndExpectComboBox.addItem("kHz")

        self.lnd_qExpectLab = QLabel('品质因数：', self)
        self.lnd_qExpectLen = QLineEdit('请输入品质因数值', self)
        self.lnd_qExpectLen.setMaxLength(3)
        self.testQThread.lnd_qExpect = 100
        self.lnd_qExpectLen.setText("{}".format(self.testQThread.lnd_qExpect))
        # self.lnd_qExpectComboBox = QComboBox(self)


        self.lnd_testPurpose = QLabel(self.lnd_testPurposeData, self)
        self.lnd_testInstrument = QLabel(self.lnd_testInstrumentData, self)
        self.lnd_testStep = QLabel(self.lnd_testStepData, self)

        layout.addWidget(self.lnd_modeLab,1,0)
        layout.addWidget(self.lnd_volLab,2,0)
        layout.addWidget(self.lnd_volLen,2,1)
        layout.addWidget(self.lnd_volComboBox,2,2)
        layout.addWidget(self.lnd_freLab)
        layout.addWidget(self.lnd_freLen)
        layout.addWidget(self.lnd_freComboBox)
        layout.addWidget(self.lnd_lndExpectLab)
        layout.addWidget(self.lnd_lndExpectLen)
        layout.addWidget(self.lnd_lndExpectComboBox)
        layout.addWidget(self.lnd_qExpectLab)
        layout.addWidget(self.lnd_qExpectLen)
        # layout.addWidget(self.lnd_qExpectComboBox)

        explainLayout.addWidget(self.lnd_testPurpose)
        explainLayout.addWidget(self.lnd_testInstrument)
        explainLayout.addWidget(self.lnd_testStep)

        self.lnd_QGroupBox.setLayout(layout)
        self.lnd_explainQGroupBox.setLayout(explainLayout)

    # 二极管测试UI初始化
    def diode_testInitConfig(self):
        self.diode_QGroupBox = QGroupBox("测试参数")
        self.diode_resultQGroupBox = QGroupBox("测试结果")
        self.diode_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QGridLayout()
        explainLayout = QGridLayout()

        self.test_Mode = "Diode"
        self.diode_modeLab = QLabel("当前为二极管测试模式", self)

        self.diode_volLab = QLabel('测试电压：', self)

        self.diode_volLen = QLineEdit('请输入测试电压值', self)
        self.diode_volLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.test_VoltageValue = 1
        self.diode_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))

        self.diode_volComboBox = QComboBox(self)
        self.diode_volComboBox.addItem("V")
        self.diode_volComboBox.addItem("mV")

        self.diode_currLab = QLabel('测试电流：', self)
        self.diode_currLen = QLineEdit('请输入测试电流值', self)
        self.diode_currLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.test_CurrValue = 1
        self.diode_currLen.setText("{}".format(self.testQThread.test_CurrValue))
        self.diode_currComboBox = QComboBox(self)
        self.diode_currComboBox.addItem("A")
        self.diode_currComboBox.addItem("mA")

        self.diode_volExpectLab = QLabel('导通电压：', self)
        self.diode_volExpectLen = QLineEdit('请输入导通电压值', self)
        self.diode_volExpectLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.diode_volExpectLen.setMaxLength(3)
        self.testQThread.diode_VoltageExpect = 3
        self.diode_volExpectLen.setText("{}".format(
            self.testQThread.diode_VoltageExpect))
        self.diode_volExpectComboBox = QComboBox(self)
        self.diode_volExpectComboBox.addItem("V")
        self.diode_volExpectComboBox.addItem("mV")

        self.diode_currExpectLab = QLabel('漏电流：', self)
        self.diode_currExpectLen = QLineEdit('请输入漏电流值', self)
        self.diode_currExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.diode_currExpect = 10
        self.diode_currExpectLen.setText("{}".format(
            self.testQThread.diode_currExpect))
        self.diode_currExpectComboBox = QComboBox(self)
        self.diode_currExpectComboBox.addItem("A")
        self.diode_currExpectComboBox.addItem("mA")
        self.diode_currExpectComboBox.addItem("uA")
        self.diode_currExpectComboBox.setCurrentIndex(1)

        # self.diode_volResultLab = QLabel("导通电压测试结果：", self)
        # self.diode_volResultLab.setGeometry(560, 100, 200, 40)
        # self.diode_currResultLab = QLabel("漏电流测试结果：", self)
        # self.diode_currResultLab.setGeometry(560, 150, 200, 40)

        self.diode_testPurpose = QLabel(self.diode_testPurposeData, self)
        self.diode_testInstrument = QLabel(self.diode_testInstrumentData, self)
        self.diode_testStep = QLabel(self.diode_testStepData, self)

        layout.addWidget(self.diode_modeLab,1,0)
        layout.addWidget(self.diode_volLab,2,0)
        layout.addWidget(self.diode_volLen,2,1)
        layout.addWidget(self.diode_volComboBox,2,2)
        layout.addWidget(self.diode_currLab)
        layout.addWidget(self.diode_currLen)
        layout.addWidget(self.diode_currComboBox)
        layout.addWidget(self.diode_volExpectLab)
        layout.addWidget(self.diode_volExpectLen)
        layout.addWidget(self.diode_volExpectComboBox)
        layout.addWidget(self.diode_currExpectLab)
        layout.addWidget(self.diode_currExpectLen)
        layout.addWidget(self.diode_currExpectComboBox)

        explainLayout.addWidget(self.diode_testPurpose)
        explainLayout.addWidget(self.diode_testInstrument)
        explainLayout.addWidget(self.diode_testStep)

        self.diode_QGroupBox.setLayout(layout)
        self.diode_explainQGroupBox.setLayout(explainLayout)

    # 三极管测试UI初始化
    def bjt_testInitConfig(self):
        self.bjt_QGroupBox = QGroupBox("测试参数")
        self.bjt_resultQGroupBox = QGroupBox("测试结果")
        self.bjt_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QGridLayout()
        explainLayout = QGridLayout()

        # 提示信息
        self.bjt_modeLab = QLabel("当前为三极管测试模式", self)

        # 测试电压参数
        self.bjt_volLab = QLabel('测试电压：', self)
        self.bjt_volLen = QLineEdit('请输入测试电压值', self)
        self.bjt_volLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.test_VoltageValue = 5
        self.bjt_volLen.setText("{}".format(self.testQThread.test_VoltageValue))
        self.bjt_volComboBox = QComboBox(self)
        self.bjt_volComboBox.addItem("V")
        self.bjt_volComboBox.addItem("mV")

        # 测试电流参数
        self.bjt_currLab = QLabel('测试电流：', self)
        self.bjt_currLen = QLineEdit('请输入测试电流值', self)
        self.bjt_currLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        # self.bjt_currLen.setMaxLength(3)
        self.testQThread.test_CurrValue = 1
        self.bjt_currLen.setText("{}".format(self.testQThread.test_CurrValue))
        self.bjt_currComboBox = QComboBox(self)
        self.bjt_currComboBox.addItem("A")
        self.bjt_currComboBox.addItem("mA")

        # 导通电压期望值
        self.bjt_volExpectLab = QLabel('导通电压：', self)
        self.bjt_volExpectLen = QLineEdit('请输入导通电压值', self)
        self.bjt_volExpectLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.bjt_VoltageExpect = 3
        self.bjt_volExpectLen.setText("{}".format(self.testQThread.bjt_VoltageExpect))
        self.bjt_volExpectComboBox = QComboBox(self)
        self.bjt_volExpectComboBox.addItem("V")
        self.bjt_volExpectComboBox.addItem("mV")

        # 集电极电流i-c期望值
        self.bjt_currExpectLab = QLabel('集电极电流：', self)
        self.bjt_currExpectLen = QLineEdit('请输入集电极电流值', self)
        self.bjt_currExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.bjt_currExpect = 10
        self.bjt_currExpectLen.setText("{}".format(self.testQThread.bjt_currExpect))
        self.bjt_currExpectComboBox = QComboBox(self)
        self.bjt_currExpectComboBox.addItem("A")
        self.bjt_currExpectComboBox.addItem("mA")
        self.bjt_currExpectComboBox.addItem("uA")
        self.bjt_currExpectComboBox.setCurrentIndex(1)

        # 放大倍数β期望值
        self.bjt_betaExpectLab = QLabel('放大倍数β：', self)
        self.bjt_betaExpectLen = QLineEdit('请输入放大倍数β值', self)
        self.bjt_betaExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.bjt_betaExpect = 300
        self.bjt_betaExpectLen.setText("{}".format(self.testQThread.bjt_betaExpect))
        # self.bjt_betaExpectComboBox = QComboBox(self)

        self.bjt_testPurpose = QLabel(self.bjt_testPurposeData, self)
        self.bjt_testInstrument = QLabel(self.bjt_testInstrumentData, self)
        self.bjt_testStep = QLabel(self.bjt_testStepData, self)

        layout.addWidget(self.bjt_modeLab,1,0)
        layout.addWidget(self.bjt_volLab,2,0)
        layout.addWidget(self.bjt_volLen,2,1)
        layout.addWidget(self.bjt_volComboBox,2,2)
        layout.addWidget(self.bjt_currLab)
        layout.addWidget(self.bjt_currLen)
        layout.addWidget(self.bjt_currComboBox)
        layout.addWidget(self.bjt_volExpectLab)
        layout.addWidget(self.bjt_volExpectLen)
        layout.addWidget(self.bjt_volExpectComboBox)
        layout.addWidget(self.bjt_currExpectLab)
        layout.addWidget(self.bjt_currExpectLen)
        layout.addWidget(self.bjt_currExpectComboBox)
        layout.addWidget(self.bjt_betaExpectLab)
        layout.addWidget(self.bjt_betaExpectLen)
        # layout.addWidget(self.bjt_betaExpectComboBox)

        explainLayout.addWidget(self.bjt_testPurpose)
        explainLayout.addWidget(self.bjt_testInstrument)
        explainLayout.addWidget(self.bjt_testStep)

        self.bjt_QGroupBox.setLayout(layout)
        self.bjt_explainQGroupBox.setLayout(explainLayout)

    # 场效应管测试UI初始化
    def mos_testInitConfig(self):
        self.mos_QGroupBox = QGroupBox("测试参数")
        self.mos_resultQGroupBox = QGroupBox("测试结果")
        self.mos_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QGridLayout()
        explainLayout = QGridLayout()

        # 提示信息
        self.mos_modeLab = QLabel("当前为场效应管测试模式", self)

        # 测试电压参数
        self.mos_volLab = QLabel('测试电压：', self)
        self.mos_volLen = QLineEdit('请输入测试电压值', self)
        self.mos_volLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.test_VoltageValue = 5
        self.mos_volLen.setText("{}".format(self.testQThread.test_VoltageValue))
        self.mos_volComboBox = QComboBox(self)
        self.mos_volComboBox.addItem("V")
        self.mos_volComboBox.addItem("mV")

        # 测试电流参数
        self.mos_currLab = QLabel('测试电流：', self)
        self.mos_currLen = QLineEdit('请输入测试电流值', self)
        self.mos_currLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        # self.mos_currLen.setMaxLength(3)
        self.testQThread.test_CurrValue = 1
        self.mos_currLen.setText("{}".format(self.testQThread.test_CurrValue))
        self.mos_currComboBox = QComboBox(self)
        self.mos_currComboBox.addItem("A")
        self.mos_currComboBox.addItem("mA")

        # 导通电压期望值
        self.mos_volExpectLab = QLabel('导通电压：', self)
        self.mos_volExpectLen = QLineEdit('请输入导通电压值', self)
        self.mos_volExpectLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.mos_volExpectLen.setMaxLength(3)
        self.testQThread.mos_VoltageExpect = 3
        self.mos_volExpectLen.setText("{}".format(self.testQThread.mos_VoltageExpect))
        self.mos_volExpectComboBox = QComboBox(self)
        self.mos_volExpectComboBox.addItem("V")
        self.mos_volExpectComboBox.addItem("mV")

        self.mos_resExpectLab = QLabel('导通电阻：', self)
        self.mos_resExpectLen = QLineEdit('请输入导通电阻值', self)
        self.mos_resExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.mos_resExpect = 10
        self.mos_resExpectLen.setText("{}".format(self.testQThread.mos_resExpect))
        self.mos_resExpectComboBox = QComboBox(self)
        self.mos_resExpectComboBox.addItem("Ω")
        self.mos_resExpectComboBox.addItem("mΩ")

        self.mos_testPurpose = QLabel(self.mos_testPurposeData, self)
        self.mos_testInstrument = QLabel(self.mos_testInstrumentData, self)
        self.mos_testStep = QLabel(self.mos_testStepData, self)

        layout.addWidget(self.mos_modeLab,1,0)
        layout.addWidget(self.mos_volLab,2,0)
        layout.addWidget(self.mos_volLen,2,1)
        layout.addWidget(self.mos_volComboBox,2,2)
        layout.addWidget(self.mos_currLab)
        layout.addWidget(self.mos_currLen)
        layout.addWidget(self.mos_currComboBox)
        layout.addWidget(self.mos_volExpectLab)
        layout.addWidget(self.mos_volExpectLen)
        layout.addWidget(self.mos_volExpectComboBox)
        layout.addWidget(self.mos_resExpectLab)
        layout.addWidget(self.mos_resExpectLen)
        layout.addWidget(self.mos_resExpectComboBox)

        explainLayout.addWidget(self.mos_testPurpose)
        explainLayout.addWidget(self.mos_testInstrument)
        explainLayout.addWidget(self.mos_testStep)

        self.mos_QGroupBox.setLayout(layout)
        self.mos_explainQGroupBox.setLayout(explainLayout)

    # 电阻测试参数UI配置
    def testResConfig(self):
        # 提示信息
        self.statusBar().showMessage('电阻测试模式')
        
        self.cap_QGroupBox.close()
        self.cap_resultQGroupBox.close()
        self.cap_explainQGroupBox.close()
        self.lnd_QGroupBox.close()
        self.lnd_resultQGroupBox.close()
        self.lnd_explainQGroupBox.close()
        self.diode_QGroupBox.close()
        self.diode_resultQGroupBox.close()
        self.diode_explainQGroupBox.close()
        self.bjt_QGroupBox.close()
        self.bjt_resultQGroupBox.close()
        self.bjt_explainQGroupBox.close()
        self.mos_QGroupBox.close()
        self.mos_resultQGroupBox.close()
        self.mos_explainQGroupBox.close()

        self.res_QGroupBox.show()
        self.res_resultQGroupBox.show()
        self.res_explainQGroupBox.show()
        # 
        # self.statusBar().showMessage('电阻测试模式')
        # self.res_modeLab = QLabel("当前为电阻测试模式", self)
        # self.res_modeLab.setGeometry(60, 50, 200, 40)
        # self.res_modeLab.show()

        # # 测试电压参数
        # self.res_volLab = QLabel('测试电压：', self)
        # self.res_volLab.setGeometry(60, 100, 80, 40)
        # self.res_volLab.show()
        # self.res_volLen = QLineEdit('请输入测试电压值', self)
        # # self.res_volLen.setMaxLength(3)
        # self.res_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),self)) # 按照正则表达式设定可输入的内容
        # self.res_volLen.setText("1")
        # self.testQThread.test_VoltageValue = 1
        # self.res_volLen.setGeometry(160, 100, 80, 40)
        # self.res_volLen.show()
        # self.res_volComboBox = QComboBox(self)
        # self.res_volComboBox.addItem("V")
        # self.res_volComboBox.addItem("mV")
        # self.res_volComboBox.setGeometry(260, 100, 80, 40)
        # self.res_volComboBox.show()

        # # 测试频率参数
        # self.res_freLab = QLabel('测试频率：', self)
        # self.res_freLab.setGeometry(60, 150, 80, 40)
        # self.res_freLab.show()
        # self.res_freLen = QLineEdit('请输入测试频率值', self)
        # # self.res_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.res_freLen.setMaxLength(3)
        # self.res_freLen.setText("100")
        # self.testQThread.test_freValue = 100
        # self.res_freLen.setGeometry(160, 150, 80, 40)
        # self.res_freLen.show()
        # self.res_freComboBox = QComboBox(self)
        # self.res_freComboBox.addItem("Hz")
        # self.res_freComboBox.addItem("kHz")
        # self.res_freComboBox.setGeometry(260, 150, 80, 40)
        # self.res_freComboBox.show()

        # # 接触阻抗期望值
        # self.res_resExpectLab = QLabel('接触阻抗：', self)
        # self.res_resExpectLab.setGeometry(60, 200, 80, 40)
        # self.res_resExpectLab.show()
        # self.res_resExpectLen = QLineEdit('请输入接触阻抗值', self)
        # # self.res_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.res_resExpectLen.setMaxLength(3)
        # self.res_resExpectLen.setText("100")
        # self.testQThread.res_resExpect = 100
        # self.res_resExpectLen.setGeometry(160, 200, 80, 40)
        # self.res_resExpectLen.show()
        # self.res_resExpectComboBox = QComboBox(self)
        # self.res_resExpectComboBox.addItem("MΩ")
        # self.res_resExpectComboBox.addItem("kΩ")
        # self.res_resExpectComboBox.addItem("Ω")
        # self.res_resExpectComboBox.addItem("mΩ")
        # self.res_resExpectComboBox.setCurrentIndex(2) # 设置默认单位值
        # self.res_resExpectComboBox.setGeometry(260, 200, 80, 40)
        # self.res_resExpectComboBox.show()

        # # 测试说明
        # self.res_testPurpose = QLabel(self.res_testPurposeData, self)
        # self.res_testPurpose.setGeometry(60, 350, 200, 40)
        # self.res_testPurpose.adjustSize()
        # self.res_testPurpose.show()
        # self.res_testInstrument = QLabel(self.res_testInstrumentData, self)
        # self.res_testInstrument.setGeometry(60, 380, 200, 40)
        # self.res_testInstrument.adjustSize()
        # self.res_testInstrument.show()
        # self.res_testStep = QLabel(self.res_testStepData, self)
        # self.res_testStep.setGeometry(60, 410, 200, 40)
        # self.res_testStep.adjustSize()
        # self.res_testStep.show()

        # # 删除控件
        # match self.test_Mode:
        #     case "Cap":
        #         self.cap_modeLab.deleteLater()
        #         self.cap_volLab.deleteLater()
        #         self.cap_volLen.deleteLater()
        #         self.cap_volComboBox.deleteLater()
        #         self.cap_freLab.deleteLater()
        #         self.cap_freLen.deleteLater()
        #         self.cap_freComboBox.deleteLater()
        #         self.cap_testPurpose.deleteLater()
        #         self.cap_testInstrument.deleteLater()
        #         self.cap_testStep.deleteLater()
        #         self.cap_capExpectLab.deleteLater()
        #         self.cap_capExpectLen.deleteLater()
        #         self.cap_capExpectComboBox.deleteLater()
        #         self.cap_esrExpectLab.deleteLater()
        #         self.cap_esrExpectLen.deleteLater()
        #         self.cap_esrExpectComboBox.deleteLater()
        #         # return
        #     case "Lnd":
        #         self.lnd_modeLab.deleteLater()
        #         self.lnd_volLab.deleteLater()
        #         self.lnd_volLen.deleteLater()
        #         self.lnd_volComboBox.deleteLater()
        #         self.lnd_freLab.deleteLater()
        #         self.lnd_freLen.deleteLater()
        #         self.lnd_freComboBox.deleteLater()
        #         self.lnd_testPurpose.deleteLater()
        #         self.lnd_testInstrument.deleteLater()
        #         self.lnd_testStep.deleteLater()
        #         self.lnd_lndExpectLab.deleteLater()
        #         self.lnd_lndExpectLen.deleteLater()
        #         self.lnd_lndExpectComboBox.deleteLater()
        #         self.lnd_qExpectLab.deleteLater()
        #         self.lnd_qExpectLen.deleteLater()
        #         # self.lnd_qExpectComboBox.deleteLater()
        #         # return
        #     case "Diode":
        #         self.diode_volLab.deleteLater()
        #         self.diode_volLen.deleteLater()
        #         self.diode_volComboBox.deleteLater()
        #         self.diode_currLab.deleteLater()
        #         self.diode_currLen.deleteLater()
        #         self.diode_currComboBox.deleteLater()
        #         self.diode_modeLab.deleteLater()
        #         self.diode_testPurpose.deleteLater()
        #         self.diode_testInstrument.deleteLater()
        #         self.diode_testStep.deleteLater()
        #         self.diode_volExpectLab.deleteLater()
        #         self.diode_volExpectLen.deleteLater()
        #         self.diode_volExpectComboBox.deleteLater()
        #         self.diode_currExpectLab.deleteLater()
        #         self.diode_currExpectLen.deleteLater()
        #         self.diode_currExpectComboBox.deleteLater()
        #         # return
        #     case "Bjt":
        #         self.bjt_volLab.deleteLater()
        #         self.bjt_volLen.deleteLater()
        #         self.bjt_volComboBox.deleteLater()
        #         self.bjt_currLab.deleteLater()
        #         self.bjt_currLen.deleteLater()
        #         self.bjt_currComboBox.deleteLater()
        #         self.bjt_modeLab.deleteLater()
        #         self.bjt_testPurpose.deleteLater()
        #         self.bjt_testInstrument.deleteLater()
        #         self.bjt_testStep.deleteLater()
        #         self.bjt_volExpectLab.deleteLater()
        #         self.bjt_volExpectLen.deleteLater()
        #         self.bjt_volExpectComboBox.deleteLater()
        #         self.bjt_currExpectLab.deleteLater()
        #         self.bjt_currExpectLen.deleteLater()
        #         self.bjt_currExpectComboBox.deleteLater()
        #         self.bjt_betaExpectLab.deleteLater()
        #         self.bjt_betaExpectLen.deleteLater()
        #         # self.bjt_betaExpectComboBox.deleteLater()
        #         # return
        #     case "Mos":
        #         self.mos_volLab.deleteLater()
        #         self.mos_volLen.deleteLater()
        #         self.mos_volComboBox.deleteLater()
        #         self.mos_currLab.deleteLater()
        #         self.mos_currLen.deleteLater()
        #         self.mos_currComboBox.deleteLater()
        #         self.mos_modeLab.deleteLater()
        #         self.mos_testPurpose.deleteLater()
        #         self.mos_testInstrument.deleteLater()
        #         self.mos_testStep.deleteLater()
        #         self.mos_volExpectLab.deleteLater()
        #         self.mos_volExpectLen.deleteLater()
        #         self.mos_volExpectComboBox.deleteLater()
        #         self.mos_resExpectLab.deleteLater()
        #         self.mos_resExpectLen.deleteLater()
        #         self.mos_resExpectComboBox.deleteLater()
        #         # return

        self.test_Mode = "Res"

    # 电容测试参数UI配置
    def testCapConfig(self):
        self.statusBar().showMessage('电容测试模式')
        self.res_QGroupBox.close()
        self.res_resultQGroupBox.close()
        self.res_explainQGroupBox.close()
        self.lnd_QGroupBox.close()
        self.lnd_resultQGroupBox.close()
        self.lnd_explainQGroupBox.close()
        self.diode_QGroupBox.close()
        self.diode_resultQGroupBox.close()
        self.diode_explainQGroupBox.close()
        self.bjt_QGroupBox.close()
        self.bjt_resultQGroupBox.close()
        self.bjt_explainQGroupBox.close()
        self.mos_QGroupBox.close()
        self.mos_resultQGroupBox.close()
        self.mos_explainQGroupBox.close()

        self.cap_QGroupBox.show()
        self.cap_resultQGroupBox.show()
        self.cap_explainQGroupBox.show()


        # # 提示信息
        # self.statusBar().showMessage('电容测试模式')
        # self.cap_modeLab = QLabel("当前为电容测试模式", self)
        # self.cap_modeLab.setGeometry(60, 50, 200, 40)
        # self.cap_modeLab.show()

        # # 测试电压参数
        # self.cap_volLab = QLabel('测试电压：', self)
        # self.cap_volLab.setGeometry(60, 100, 80, 40)
        # self.cap_volLab.show()
        # self.cap_volLen = QLineEdit('请输入测试电压值', self)
        # # self.cap_volLen.setMaxLength(3)
        # self.cap_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),self)) # 按照正则表达式设定可输入的内容
        # self.cap_volLen.setText("1")
        # self.testQThread.test_VoltageValue = 1
        # self.cap_volLen.setGeometry(160, 100, 80, 40)
        # self.cap_volLen.show()
        # self.cap_volComboBox = QComboBox(self)
        # self.cap_volComboBox.addItem("V")
        # self.cap_volComboBox.addItem("mV")
        # self.cap_volComboBox.setGeometry(260, 100, 80, 40)
        # self.cap_volComboBox.show()

        # # 测试频率参数
        # self.cap_freLab = QLabel('测试频率：', self)
        # self.cap_freLab.setGeometry(60, 150, 80, 40)
        # self.cap_freLab.show()
        # self.cap_freLen = QLineEdit('请输入测试频率值', self)
        # # self.cap_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.cap_freLen.setMaxLength(3)
        # self.cap_freLen.setText("100")
        # self.testQThread.test_freValue = 100
        # self.cap_freLen.setGeometry(160, 150, 80, 40)
        # self.cap_freLen.show()
        # self.cap_freComboBox = QComboBox(self)
        # self.cap_freComboBox.addItem("Hz")
        # self.cap_freComboBox.addItem("kHz")
        # self.cap_freComboBox.setGeometry(260, 150, 80, 40)
        # self.cap_freComboBox.show()

        # # 电容量期望值
        # self.cap_capExpectLab = QLabel('电容值：', self)
        # self.cap_capExpectLab.setGeometry(60, 200, 80, 40)
        # self.cap_capExpectLab.show()
        # self.cap_capExpectLen = QLineEdit('请输入电容值', self)
        # # self.cap_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.cap_capExpectLen.setMaxLength(3)
        # self.cap_capExpectLen.setText("100")
        # self.testQThread.cap_capExpect = 100
        # self.cap_capExpectLen.setGeometry(160, 200, 80, 40)
        # self.cap_capExpectLen.show()
        # self.cap_capExpectComboBox = QComboBox(self)
        # self.cap_capExpectComboBox.addItem("F")
        # self.cap_capExpectComboBox.addItem("mF")
        # self.cap_capExpectComboBox.addItem("uF")
        # self.cap_capExpectComboBox.addItem("nF")
        # self.cap_capExpectComboBox.addItem("pF")
        # self.cap_capExpectComboBox.setCurrentIndex(2)
        # self.cap_capExpectComboBox.setGeometry(260, 200, 80, 40)
        # self.cap_capExpectComboBox.show()

        # # 等效串联电阻期望值
        # self.cap_esrExpectLab = QLabel('ESR：', self)
        # self.cap_esrExpectLab.setGeometry(60, 250, 80, 40)
        # self.cap_esrExpectLab.show()
        # self.cap_esrExpectLen = QLineEdit('请输入等效串联电阻值', self)
        # # self.cap_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.cap_esrExpectLen.setMaxLength(3)
        # self.cap_esrExpectLen.setText("100")
        # self.testQThread.cap_esrExpect = 100
        # self.cap_esrExpectLen.setGeometry(160, 250, 80, 40)
        # self.cap_esrExpectLen.show()
        # self.cap_esrExpectComboBox = QComboBox(self)
        # self.cap_esrExpectComboBox.addItem("kΩ")
        # self.cap_esrExpectComboBox.addItem("Ω")
        # self.cap_esrExpectComboBox.addItem("mΩ")
        # self.cap_esrExpectComboBox.setCurrentIndex(1)
        # self.cap_esrExpectComboBox.setGeometry(260, 250, 80, 40)
        # self.cap_esrExpectComboBox.show()

        # # 测试说明
        # self.cap_testPurpose = QLabel(self.cap_testPurposeData, self)
        # self.cap_testPurpose.setGeometry(60, 350, 200, 40)
        # self.cap_testPurpose.adjustSize()
        # self.cap_testPurpose.show()
        # self.cap_testInstrument = QLabel(self.cap_testInstrumentData, self)
        # self.cap_testInstrument.setGeometry(60, 380, 200, 40)
        # self.cap_testInstrument.adjustSize()
        # self.cap_testInstrument.show()
        # self.cap_testStep = QLabel(self.cap_testStepData, self)
        # self.cap_testStep.setGeometry(60, 410, 200, 40)
        # self.cap_testStep.adjustSize()
        # self.cap_testStep.show()
        # # 删除控件
        # match self.test_Mode:
        #     case "Res":
        #         self.res_modeLab.deleteLater()
        #         self.res_volLab.deleteLater()
        #         self.res_volLen.deleteLater()
        #         self.res_volComboBox.deleteLater()
        #         self.res_freLab.deleteLater()
        #         self.res_freLen.deleteLater()
        #         self.res_freComboBox.deleteLater()
        #         self.res_testPurpose.deleteLater()
        #         self.res_testInstrument.deleteLater()
        #         self.res_testStep.deleteLater()
        #         self.res_resExpectLab.deleteLater()
        #         self.res_resExpectLen.deleteLater()
        #         self.res_resExpectComboBox.deleteLater()
        #         # return
        #     case "Lnd":
        #         self.lnd_modeLab.deleteLater()
        #         self.lnd_volLab.deleteLater()
        #         self.lnd_volLen.deleteLater()
        #         self.lnd_volComboBox.deleteLater()
        #         self.lnd_freLab.deleteLater()
        #         self.lnd_freLen.deleteLater()
        #         self.lnd_freComboBox.deleteLater()
        #         self.lnd_testPurpose.deleteLater()
        #         self.lnd_testInstrument.deleteLater()
        #         self.lnd_testStep.deleteLater()
        #         self.lnd_lndExpectLab.deleteLater()
        #         self.lnd_lndExpectLen.deleteLater()
        #         self.lnd_lndExpectComboBox.deleteLater()
        #         self.lnd_qExpectLab.deleteLater()
        #         self.lnd_qExpectLen.deleteLater()
        #         # self.lnd_qExpectComboBox.deleteLater()
        #         # return
        #     case "Diode":
        #         self.diode_volLab.deleteLater()
        #         self.diode_volLen.deleteLater()
        #         self.diode_volComboBox.deleteLater()
        #         self.diode_currLab.deleteLater()
        #         self.diode_currLen.deleteLater()
        #         self.diode_currComboBox.deleteLater()
        #         self.diode_modeLab.deleteLater()
        #         self.diode_testPurpose.deleteLater()
        #         self.diode_testInstrument.deleteLater()
        #         self.diode_testStep.deleteLater()
        #         self.diode_volExpectLab.deleteLater()
        #         self.diode_volExpectLen.deleteLater()
        #         self.diode_volExpectComboBox.deleteLater()
        #         self.diode_currExpectLab.deleteLater()
        #         self.diode_currExpectLen.deleteLater()
        #         self.diode_currExpectComboBox.deleteLater()
        #         # return
        #     case "Bjt":
        #         self.bjt_volLab.deleteLater()
        #         self.bjt_volLen.deleteLater()
        #         self.bjt_volComboBox.deleteLater()
        #         self.bjt_currLab.deleteLater()
        #         self.bjt_currLen.deleteLater()
        #         self.bjt_currComboBox.deleteLater()
        #         self.bjt_modeLab.deleteLater()
        #         self.bjt_testPurpose.deleteLater()
        #         self.bjt_testInstrument.deleteLater()
        #         self.bjt_testStep.deleteLater()
        #         self.bjt_volExpectLab.deleteLater()
        #         self.bjt_volExpectLen.deleteLater()
        #         self.bjt_volExpectComboBox.deleteLater()
        #         self.bjt_currExpectLab.deleteLater()
        #         self.bjt_currExpectLen.deleteLater()
        #         self.bjt_currExpectComboBox.deleteLater()
        #         self.bjt_betaExpectLab.deleteLater()
        #         self.bjt_betaExpectLen.deleteLater()
        #         # self.bjt_betaExpectComboBox.deleteLater()
        #         # return
        #     case "Mos":
        #         self.mos_volLab.deleteLater()
        #         self.mos_volLen.deleteLater()
        #         self.mos_volComboBox.deleteLater()
        #         self.mos_currLab.deleteLater()
        #         self.mos_currLen.deleteLater()
        #         self.mos_currComboBox.deleteLater()
        #         self.mos_modeLab.deleteLater()
        #         self.mos_testPurpose.deleteLater()
        #         self.mos_testInstrument.deleteLater()
        #         self.mos_testStep.deleteLater()
        #         self.mos_volExpectLab.deleteLater()
        #         self.mos_volExpectLen.deleteLater()
        #         self.mos_volExpectComboBox.deleteLater()
        #         self.mos_resExpectLab.deleteLater()
        #         self.mos_resExpectLen.deleteLater()
        #         self.mos_resExpectComboBox.deleteLater()
        # return

        self.test_Mode = "Cap"

    # 电感测试参数UI配置
    def testLndConfig(self):
        self.statusBar().showMessage('电感测试模式')
        self.res_QGroupBox.close()
        self.res_resultQGroupBox.close()
        self.res_explainQGroupBox.close()
        self.cap_QGroupBox.close()
        self.cap_resultQGroupBox.close()
        self.cap_explainQGroupBox.close()
        self.diode_QGroupBox.close()
        self.diode_resultQGroupBox.close()
        self.diode_explainQGroupBox.close()
        self.bjt_QGroupBox.close()
        self.bjt_resultQGroupBox.close()
        self.bjt_explainQGroupBox.close()
        self.mos_QGroupBox.close()
        self.mos_resultQGroupBox.close()
        self.mos_explainQGroupBox.close()

        self.lnd_QGroupBox.show()
        self.lnd_resultQGroupBox.show()
        self.lnd_explainQGroupBox.show()
        # # 提示信息
        # self.statusBar().showMessage('电感测试模式')
        # self.lnd_modeLab = QLabel("当前为电感测试模式", self)
        # self.lnd_modeLab.setGeometry(60, 50, 200, 40)
        # self.lnd_modeLab.show()

        # # 测试电压参数
        # self.lnd_volLab = QLabel('测试电压：', self)
        # self.lnd_volLab.setGeometry(60, 100, 80, 40)
        # self.lnd_volLab.show()
        # self.lnd_volLen = QLineEdit('请输入测试电压值', self)
        # # self.lnd_volLen.setMaxLength(3)
        # self.lnd_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),self)) # 按照正则表达式设定可输入的内容
        # self.lnd_volLen.setText("1")
        # self.testQThread.test_VoltageValue = 1
        # self.lnd_volLen.setGeometry(160, 100, 80, 40)
        # self.lnd_volLen.show()
        # self.lnd_volComboBox = QComboBox(self)
        # self.lnd_volComboBox.addItem("V")
        # self.lnd_volComboBox.addItem("mV")
        # self.lnd_volComboBox.setGeometry(260, 100, 80, 40)
        # self.lnd_volComboBox.show()

        # # 测试频率参数
        # self.lnd_freLab = QLabel('测试频率：', self)
        # self.lnd_freLab.setGeometry(60, 150, 80, 40)
        # self.lnd_freLab.show()
        # self.lnd_freLen = QLineEdit('请输入测试频率值', self)
        # # self.lnd_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.lnd_freLen.setMaxLength(3)
        # self.lnd_freLen.setText("100")
        # self.testQThread.test_freValue = 100
        # self.lnd_freLen.setGeometry(160, 150, 80, 40)
        # self.lnd_freLen.show()
        # self.lnd_freComboBox = QComboBox(self)
        # self.lnd_freComboBox.addItem("Hz")
        # self.lnd_freComboBox.addItem("kHz")
        # self.lnd_freComboBox.setGeometry(260, 150, 80, 40)
        # self.lnd_freComboBox.show()

        # # 电感量期望值
        # self.lnd_lndExpectLab = QLabel('电感值：', self)
        # self.lnd_lndExpectLab.setGeometry(60, 200, 80, 40)
        # self.lnd_lndExpectLab.show()
        # self.lnd_lndExpectLen = QLineEdit('请输入电感值', self)
        # # self.lnd_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.lnd_lndExpectLen.setMaxLength(3)
        # self.lnd_lndExpectLen.setText("100")
        # self.testQThread.lnd_lndExpect = 100
        # self.lnd_lndExpectLen.setGeometry(160, 200, 80, 40)
        # self.lnd_lndExpectLen.show()
        # self.lnd_lndExpectComboBox = QComboBox(self)
        # self.lnd_lndExpectComboBox.addItem("Hz")
        # self.lnd_lndExpectComboBox.addItem("kHz")
        # self.lnd_lndExpectComboBox.setGeometry(260, 200, 80, 40)
        # self.lnd_lndExpectComboBox.show()

        # # 品质因数期望值
        # self.lnd_qExpectLab = QLabel('品质因数：', self)
        # self.lnd_qExpectLab.setGeometry(60, 250, 80, 40)
        # self.lnd_qExpectLab.show()
        # self.lnd_qExpectLen = QLineEdit('请输入品质因数值', self)
        # # self.lnd_volLen.setValidator(QRegExpValidator(QRegExp("[0-9][0-9][0-9]"), self))
        # self.lnd_qExpectLen.setMaxLength(3)
        # self.lnd_qExpectLen.setText("100")
        # self.testQThread.lnd_qExpect = 100
        # self.lnd_qExpectLen.setGeometry(160, 250, 80, 40)
        # self.lnd_qExpectLen.show()
        # # self.lnd_qExpectComboBox = QComboBox(self)
        # # self.lnd_qExpectComboBox.addItem("Hz")
        # # self.lnd_qExpectComboBox.addItem("kHz")
        # # self.lnd_qExpectComboBox.setGeometry(260, 250, 80, 40)
        # # self.lnd_qExpectComboBox.show()

        # # 测试说明
        # self.lnd_testPurpose = QLabel(self.lnd_testPurposeData, self)
        # self.lnd_testPurpose.setGeometry(60, 350, 200, 40)
        # self.lnd_testPurpose.adjustSize()
        # self.lnd_testPurpose.show()
        # self.lnd_testInstrument = QLabel(self.lnd_testInstrumentData, self)
        # self.lnd_testInstrument.setGeometry(60, 380, 200, 40)
        # self.lnd_testInstrument.adjustSize()
        # self.lnd_testInstrument.show()
        # self.lnd_testStep = QLabel(self.lnd_testStepData, self)
        # self.lnd_testStep.setGeometry(60, 410, 200, 40)
        # self.lnd_testStep.adjustSize()
        # self.lnd_testStep.show()

        # # 删除控件
        # match self.test_Mode:
        #     case "Res":
        #         self.res_modeLab.deleteLater()
        #         self.res_volLab.deleteLater()
        #         self.res_volLen.deleteLater()
        #         self.res_volComboBox.deleteLater()
        #         self.res_freLab.deleteLater()
        #         self.res_freLen.deleteLater()
        #         self.res_freComboBox.deleteLater()
        #         self.res_testPurpose.deleteLater()
        #         self.res_testInstrument.deleteLater()
        #         self.res_testStep.deleteLater()
        #         self.res_resExpectLab.deleteLater()
        #         self.res_resExpectLen.deleteLater()
        #         self.res_resExpectComboBox.deleteLater()
        #         # return
        #     case "Cap":
        #         self.cap_modeLab.deleteLater()
        #         self.cap_volLab.deleteLater()
        #         self.cap_volLen.deleteLater()
        #         self.cap_volComboBox.deleteLater()
        #         self.cap_freLab.deleteLater()
        #         self.cap_freLen.deleteLater()
        #         self.cap_freComboBox.deleteLater()
        #         self.cap_testPurpose.deleteLater()
        #         self.cap_testInstrument.deleteLater()
        #         self.cap_testStep.deleteLater()
        #         self.cap_capExpectLab.deleteLater()
        #         self.cap_capExpectLen.deleteLater()
        #         self.cap_capExpectComboBox.deleteLater()
        #         self.cap_esrExpectLab.deleteLater()
        #         self.cap_esrExpectLen.deleteLater()
        #         self.cap_esrExpectComboBox.deleteLater()
        #         # return
        #     case "Diode":
        #         self.diode_volLab.deleteLater()
        #         self.diode_volLen.deleteLater()
        #         self.diode_volComboBox.deleteLater()
        #         self.diode_currLab.deleteLater()
        #         self.diode_currLen.deleteLater()
        #         self.diode_currComboBox.deleteLater()
        #         self.diode_modeLab.deleteLater()
        #         self.diode_testPurpose.deleteLater()
        #         self.diode_testInstrument.deleteLater()
        #         self.diode_testStep.deleteLater()
        #         self.diode_volExpectLab.deleteLater()
        #         self.diode_volExpectLen.deleteLater()
        #         self.diode_volExpectComboBox.deleteLater()
        #         self.diode_currExpectLab.deleteLater()
        #         self.diode_currExpectLen.deleteLater()
        #         self.diode_currExpectComboBox.deleteLater()
        #         # return
        #     case "Bjt":
        #         self.bjt_volLab.deleteLater()
        #         self.bjt_volLen.deleteLater()
        #         self.bjt_volComboBox.deleteLater()
        #         self.bjt_currLab.deleteLater()
        #         self.bjt_currLen.deleteLater()
        #         self.bjt_currComboBox.deleteLater()
        #         self.bjt_modeLab.deleteLater()
        #         self.bjt_testPurpose.deleteLater()
        #         self.bjt_testInstrument.deleteLater()
        #         self.bjt_testStep.deleteLater()
        #         self.bjt_volExpectLab.deleteLater()
        #         self.bjt_volExpectLen.deleteLater()
        #         self.bjt_volExpectComboBox.deleteLater()
        #         self.bjt_currExpectLab.deleteLater()
        #         self.bjt_currExpectLen.deleteLater()
        #         self.bjt_currExpectComboBox.deleteLater()
        #         self.bjt_betaExpectLab.deleteLater()
        #         self.bjt_betaExpectLen.deleteLater()
        #         # self.bjt_betaExpectComboBox.deleteLater()
        #         # return
        #     case "Mos":
        #         self.mos_volLab.deleteLater()
        #         self.mos_volLen.deleteLater()
        #         self.mos_volComboBox.deleteLater()
        #         self.mos_currLab.deleteLater()
        #         self.mos_currLen.deleteLater()
        #         self.mos_currComboBox.deleteLater()
        #         self.mos_modeLab.deleteLater()
        #         self.mos_testPurpose.deleteLater()
        #         self.mos_testInstrument.deleteLater()
        #         self.mos_testStep.deleteLater()
        #         self.mos_volExpectLab.deleteLater()
        #         self.mos_volExpectLen.deleteLater()
        #         self.mos_volExpectComboBox.deleteLater()
        #         self.mos_resExpectLab.deleteLater()
        #         self.mos_resExpectLen.deleteLater()
        #         self.mos_resExpectComboBox.deleteLater()
        #         # return

        self.test_Mode = "Lnd"

    # 二极管测试参数UI配置
    def testDiodeConfig(self):
        self.statusBar().showMessage('二极管测试模式')
        self.res_QGroupBox.close()
        self.res_resultQGroupBox.close()
        self.res_explainQGroupBox.close()
        self.cap_QGroupBox.close()
        self.cap_resultQGroupBox.close()
        self.cap_explainQGroupBox.close()
        self.lnd_QGroupBox.close()
        self.lnd_resultQGroupBox.close()
        self.lnd_explainQGroupBox.close()
        self.bjt_QGroupBox.close()
        self.bjt_resultQGroupBox.close()
        self.bjt_explainQGroupBox.close()
        self.mos_QGroupBox.close()
        self.mos_resultQGroupBox.close()
        self.mos_explainQGroupBox.close()

        self.diode_QGroupBox.show()
        self.diode_resultQGroupBox.show()
        self.diode_explainQGroupBox.show()
        # # 提示信息
        # self.statusBar().showMessage('二极管测试模式')
        # self.diode_modeLab = QLabel("当前为二极管测试模式", self)
        # self.diode_modeLab.setGeometry(60, 50, 200, 40)
        # self.diode_modeLab.show()

        # # 测试电压参数
        # self.diode_volLab = QLabel('测试电压：', self)
        # self.diode_volLab.setGeometry(60, 100, 80, 40)
        # self.diode_volLab.show()
        # self.diode_volLen = QLineEdit('请输入测试电压值', self)
        # self.diode_volLen.setValidator(QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.diode_volLen.setText("5")
        # self.testQThread.test_VoltageValue = 5
        # self.diode_volLen.setGeometry(160, 100, 80, 40)
        # self.diode_volLen.show()
        # self.diode_volComboBox = QComboBox(self)
        # self.diode_volComboBox.addItem("V")
        # self.diode_volComboBox.addItem("mV")
        # self.diode_volComboBox.setGeometry(260, 100, 80, 40)
        # self.diode_volComboBox.show()

        # # 测试电流参数
        # self.diode_currLab = QLabel('测试电流：', self)
        # self.diode_currLab.setGeometry(60, 150, 80, 40)
        # self.diode_currLab.show()
        # self.diode_currLen = QLineEdit('请输入测试电流值', self)
        # self.diode_currLen.setValidator(QRegExpValidator(QRegExp("[0-9]|10"), self))
        # # self.diode_currLen.setMaxLength(3)
        # self.diode_currLen.setText("1")
        # self.testQThread.test_CurrValue = 1
        # self.diode_currLen.setGeometry(160, 150, 80, 40)
        # self.diode_currLen.show()
        # self.diode_currComboBox = QComboBox(self)
        # self.diode_currComboBox.addItem("A")
        # self.diode_currComboBox.addItem("mA")
        # self.diode_currComboBox.setGeometry(260, 150, 80, 40)
        # self.diode_currComboBox.show()

        # # 导通电压期望值
        # self.diode_volExpectLab = QLabel('导通电压：', self)
        # self.diode_volExpectLab.setGeometry(60, 200, 80, 40)
        # self.diode_volExpectLab.show()
        # self.diode_volExpectLen = QLineEdit('请输入导通电压值', self)
        # self.diode_volExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # # self.diode_volExpectLen.setMaxLength(3)
        # self.diode_volExpectLen.setText("3")
        # self.testQThread.diode_VoltageExpect = 3
        # self.diode_volExpectLen.setGeometry(160, 200, 80, 40)
        # self.diode_volExpectLen.show()
        # self.diode_volExpectComboBox = QComboBox(self)
        # self.diode_volExpectComboBox.addItem("V")
        # self.diode_volExpectComboBox.addItem("mV")
        # self.diode_volExpectComboBox.setGeometry(260, 200, 80, 40)
        # self.diode_volExpectComboBox.show()

        # # 漏电流期望值
        # self.diode_currExpectLab = QLabel('漏电流：', self)
        # self.diode_currExpectLab.setGeometry(60, 250, 80, 40)
        # self.diode_currExpectLab.show()
        # self.diode_currExpectLen = QLineEdit('请输入漏电流值', self)
        # self.diode_currExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("[0-9]|10"), self))
        # self.diode_currExpectLen.setText("10")
        # self.testQThread.diode_currExpect = 10
        # self.diode_currExpectLen.setGeometry(160, 250, 80, 40)
        # self.diode_currExpectLen.show()
        # self.diode_currExpectComboBox = QComboBox(self)
        # self.diode_currExpectComboBox.addItem("A")
        # self.diode_currExpectComboBox.addItem("mA")
        # self.diode_currExpectComboBox.addItem("uA")
        # self.diode_currExpectComboBox.setCurrentIndex(1)
        # self.diode_currExpectComboBox.setGeometry(260, 250, 80, 40)
        # self.diode_currExpectComboBox.show()

        # # 测试说明
        # self.diode_testPurpose = QLabel(self.diode_testPurposeData, self)
        # self.diode_testPurpose.setGeometry(60, 350, 200, 40)
        # self.diode_testPurpose.adjustSize()
        # self.diode_testPurpose.show()
        # self.diode_testInstrument = QLabel(self.diode_testInstrumentData, self)
        # self.diode_testInstrument.setGeometry(60, 380, 200, 40)
        # self.diode_testInstrument.adjustSize()
        # self.diode_testInstrument.show()
        # self.diode_testStep = QLabel(self.diode_testStepData, self)
        # self.diode_testStep.setGeometry(60, 410, 200, 40)
        # self.diode_testStep.adjustSize()
        # self.diode_testStep.show()

        # # 删除控件
        # match self.test_Mode:
        #     case "Res":
        #         self.res_modeLab.deleteLater()
        #         self.res_volLab.deleteLater()
        #         self.res_volLen.deleteLater()
        #         self.res_volComboBox.deleteLater()
        #         self.res_freLab.deleteLater()
        #         self.res_freLen.deleteLater()
        #         self.res_freComboBox.deleteLater()
        #         self.res_testPurpose.deleteLater()
        #         self.res_testInstrument.deleteLater()
        #         self.res_testStep.deleteLater()
        #         self.res_resExpectLab.deleteLater()
        #         self.res_resExpectLen.deleteLater()
        #         self.res_resExpectComboBox.deleteLater()
        #         # return
        #     case "Cap":
        #         self.cap_modeLab.deleteLater()
        #         self.cap_volLab.deleteLater()
        #         self.cap_volLen.deleteLater()
        #         self.cap_volComboBox.deleteLater()
        #         self.cap_freLab.deleteLater()
        #         self.cap_freLen.deleteLater()
        #         self.cap_freComboBox.deleteLater()
        #         self.cap_testPurpose.deleteLater()
        #         self.cap_testInstrument.deleteLater()
        #         self.cap_testStep.deleteLater()
        #         self.cap_capExpectLab.deleteLater()
        #         self.cap_capExpectLen.deleteLater()
        #         self.cap_capExpectComboBox.deleteLater()
        #         self.cap_esrExpectLab.deleteLater()
        #         self.cap_esrExpectLen.deleteLater()
        #         self.cap_esrExpectComboBox.deleteLater()
        #         # return
        #     case "Lnd":
        #         self.lnd_modeLab.deleteLater()
        #         self.lnd_volLab.deleteLater()
        #         self.lnd_volLen.deleteLater()
        #         self.lnd_volComboBox.deleteLater()
        #         self.lnd_freLab.deleteLater()
        #         self.lnd_freLen.deleteLater()
        #         self.lnd_freComboBox.deleteLater()
        #         self.lnd_testPurpose.deleteLater()
        #         self.lnd_testInstrument.deleteLater()
        #         self.lnd_testStep.deleteLater()
        #         self.lnd_lndExpectLab.deleteLater()
        #         self.lnd_lndExpectLen.deleteLater()
        #         self.lnd_lndExpectComboBox.deleteLater()
        #         self.lnd_qExpectLab.deleteLater()
        #         self.lnd_qExpectLen.deleteLater()
        #         # self.lnd_qExpectComboBox.deleteLater()
        #         # return
        #     case "Bjt":
        #         self.bjt_volLab.deleteLater()
        #         self.bjt_volLen.deleteLater()
        #         self.bjt_volComboBox.deleteLater()
        #         self.bjt_currLab.deleteLater()
        #         self.bjt_currLen.deleteLater()
        #         self.bjt_currComboBox.deleteLater()
        #         self.bjt_modeLab.deleteLater()
        #         self.bjt_testPurpose.deleteLater()
        #         self.bjt_testInstrument.deleteLater()
        #         self.bjt_testStep.deleteLater()
        #         self.bjt_volExpectLab.deleteLater()
        #         self.bjt_volExpectLen.deleteLater()
        #         self.bjt_volExpectComboBox.deleteLater()
        #         self.bjt_currExpectLab.deleteLater()
        #         self.bjt_currExpectLen.deleteLater()
        #         self.bjt_currExpectComboBox.deleteLater()
        #         self.bjt_betaExpectLab.deleteLater()
        #         self.bjt_betaExpectLen.deleteLater()
        #         # self.bjt_betaExpectComboBox.deleteLater()
        #         # return
        #     case "Mos":
        #         self.mos_volLab.deleteLater()
        #         self.mos_volLen.deleteLater()
        #         self.mos_volComboBox.deleteLater()
        #         self.mos_currLab.deleteLater()
        #         self.mos_currLen.deleteLater()
        #         self.mos_currComboBox.deleteLater()
        #         self.mos_modeLab.deleteLater()
        #         self.mos_testPurpose.deleteLater()
        #         self.mos_testInstrument.deleteLater()
        #         self.mos_testStep.deleteLater()
        #         self.mos_volExpectLab.deleteLater()
        #         self.mos_volExpectLen.deleteLater()
        #         self.mos_volExpectComboBox.deleteLater()
        #         self.mos_resExpectLab.deleteLater()
        #         self.mos_resExpectLen.deleteLater()
        #         self.mos_resExpectComboBox.deleteLater()
        #         # return

        # 设定测试模式
        self.test_Mode = "Diode"

    # 三极管测试参数UI配置
    def testBjtConfig(self):
        self.statusBar().showMessage('三极管测试模式')
        self.res_QGroupBox.close()
        self.res_resultQGroupBox.close()
        self.res_explainQGroupBox.close()
        self.cap_QGroupBox.close()
        self.cap_resultQGroupBox.close()
        self.cap_explainQGroupBox.close()
        self.lnd_QGroupBox.close()
        self.lnd_resultQGroupBox.close()
        self.lnd_explainQGroupBox.close()
        self.diode_QGroupBox.close()
        self.diode_resultQGroupBox.close()
        self.diode_explainQGroupBox.close()
        self.mos_QGroupBox.close()
        self.mos_resultQGroupBox.close()
        self.mos_explainQGroupBox.close()

        self.bjt_QGroupBox.show()
        self.bjt_resultQGroupBox.show()
        self.bjt_explainQGroupBox.show()
        # # 提示信息
        # self.statusBar().showMessage('三极管测试模式')
        # self.bjt_modeLab = QLabel("当前为三极管测试模式", self)
        # self.bjt_modeLab.setGeometry(60, 50, 200, 40)
        # self.bjt_modeLab.show()

        # # 测试电压参数
        # self.bjt_volLab = QLabel('测试电压：', self)
        # self.bjt_volLab.setGeometry(60, 100, 80, 40)
        # self.bjt_volLab.show()
        # self.bjt_volLen = QLineEdit('请输入测试电压值', self)
        # self.bjt_volLen.setValidator(
        #     QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.bjt_volLen.setText("5")
        # self.testQThread.test_VoltageValue = 5
        # self.bjt_volLen.setGeometry(160, 100, 80, 40)
        # self.bjt_volLen.show()
        # self.bjt_volComboBox = QComboBox(self)
        # self.bjt_volComboBox.addItem("V")
        # self.bjt_volComboBox.addItem("mV")
        # self.bjt_volComboBox.setGeometry(260, 100, 80, 40)
        # self.bjt_volComboBox.show()

        # # 测试电流参数
        # self.bjt_currLab = QLabel('测试电流：', self)
        # self.bjt_currLab.setGeometry(60, 150, 80, 40)
        # self.bjt_currLab.show()
        # self.bjt_currLen = QLineEdit('请输入测试电流值', self)
        # self.bjt_currLen.setValidator(
        #     QRegExpValidator(QRegExp("[0-9]|10"), self))
        # # self.bjt_currLen.setMaxLength(3)
        # self.bjt_currLen.setText("1")
        # self.testQThread.test_CurrValue = 1
        # self.bjt_currLen.setGeometry(160, 150, 80, 40)
        # self.bjt_currLen.show()
        # self.bjt_currComboBox = QComboBox(self)
        # self.bjt_currComboBox.addItem("A")
        # self.bjt_currComboBox.addItem("mA")
        # self.bjt_currComboBox.setGeometry(260, 150, 80, 40)
        # self.bjt_currComboBox.show()

        # # 导通电压期望值
        # self.bjt_volExpectLab = QLabel('导通电压：', self)
        # self.bjt_volExpectLab.setGeometry(60, 200, 80, 40)
        # self.bjt_volExpectLab.show()
        # self.bjt_volExpectLen = QLineEdit('请输入导通电压值', self)
        # self.bjt_volExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # # self.bjt_volExpectLen.setMaxLength(3)
        # self.bjt_volExpectLen.setText("3")
        # self.testQThread.bjt_VoltageExpect = 3
        # self.bjt_volExpectLen.setGeometry(160, 200, 80, 40)
        # self.bjt_volExpectLen.show()
        # self.bjt_volExpectComboBox = QComboBox(self)
        # self.bjt_volExpectComboBox.addItem("V")
        # self.bjt_volExpectComboBox.addItem("mV")
        # self.bjt_volExpectComboBox.setGeometry(260, 200, 80, 40)
        # self.bjt_volExpectComboBox.show()

        # # 集电极电流i-c期望值
        # self.bjt_currExpectLab = QLabel('集电极电流：', self)
        # self.bjt_currExpectLab.setGeometry(60, 250, 80, 40)
        # self.bjt_currExpectLab.show()
        # self.bjt_currExpectLen = QLineEdit('请输入集电极电流值', self)
        # self.bjt_currExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("[0-9]|10"), self))
        # self.bjt_currExpectLen.setText("10")
        # self.testQThread.bjt_currExpect = 10
        # self.bjt_currExpectLen.setGeometry(160, 250, 80, 40)
        # self.bjt_currExpectLen.show()
        # self.bjt_currExpectComboBox = QComboBox(self)
        # self.bjt_currExpectComboBox.addItem("A")
        # self.bjt_currExpectComboBox.addItem("mA")
        # self.bjt_currExpectComboBox.addItem("uA")
        # self.bjt_currExpectComboBox.setCurrentIndex(1)
        # self.bjt_currExpectComboBox.setGeometry(260, 250, 80, 40)
        # self.bjt_currExpectComboBox.show()

        # # 放大倍数β期望值
        # self.bjt_betaExpectLab = QLabel('放大倍数β：', self)
        # self.bjt_betaExpectLab.setGeometry(60, 300, 80, 40)
        # self.bjt_betaExpectLab.show()
        # self.bjt_betaExpectLen = QLineEdit('请输入放大倍数β值', self)
        # self.bjt_betaExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("[0-9]|10"), self))
        # self.testQThread.bjt_betaExpect = 300
        # self.bjt_betaExpectLen.setText("{}".format(self.testQThread.bjt_betaExpect))
        # self.bjt_betaExpectLen.setGeometry(160, 300, 80, 40)
        # self.bjt_betaExpectLen.show()
        # # self.bjt_betaExpectComboBox = QComboBox(self)
        # # self.bjt_betaExpectComboBox.addItem("A")
        # # self.bjt_betaExpectComboBox.addItem("mA")
        # # self.bjt_betaExpectComboBox.setGeometry(260, 300, 80, 40)
        # # self.bjt_betaExpectComboBox.show()

        # # 测试说明
        # self.bjt_testPurpose = QLabel(self.bjt_testPurposeData, self)
        # self.bjt_testPurpose.setGeometry(60, 350, 200, 40)
        # self.bjt_testPurpose.adjustSize()
        # self.bjt_testPurpose.show()
        # self.bjt_testInstrument = QLabel(self.bjt_testInstrumentData, self)
        # self.bjt_testInstrument.setGeometry(60, 380, 200, 40)
        # self.bjt_testInstrument.adjustSize()
        # self.bjt_testInstrument.show()
        # self.bjt_testStep = QLabel(self.bjt_testStepData, self)
        # self.bjt_testStep.setGeometry(60, 410, 200, 40)
        # self.bjt_testStep.adjustSize()
        # self.bjt_testStep.show()

        # # 删除控件
        # match self.test_Mode:
        #     case "Res":
        #         self.res_modeLab.deleteLater()
        #         self.res_volLab.deleteLater()
        #         self.res_volLen.deleteLater()
        #         self.res_volComboBox.deleteLater()
        #         self.res_freLab.deleteLater()
        #         self.res_freLen.deleteLater()
        #         self.res_freComboBox.deleteLater()
        #         self.res_testPurpose.deleteLater()
        #         self.res_testInstrument.deleteLater()
        #         self.res_testStep.deleteLater()
        #         self.res_resExpectLab.deleteLater()
        #         self.res_resExpectLen.deleteLater()
        #         self.res_resExpectComboBox.deleteLater()
        #         # return
        #     case "Cap":
        #         self.cap_modeLab.deleteLater()
        #         self.cap_volLab.deleteLater()
        #         self.cap_volLen.deleteLater()
        #         self.cap_volComboBox.deleteLater()
        #         self.cap_freLab.deleteLater()
        #         self.cap_freLen.deleteLater()
        #         self.cap_freComboBox.deleteLater()
        #         self.cap_testPurpose.deleteLater()
        #         self.cap_testInstrument.deleteLater()
        #         self.cap_testStep.deleteLater()
        #         self.cap_capExpectLab.deleteLater()
        #         self.cap_capExpectLen.deleteLater()
        #         self.cap_capExpectComboBox.deleteLater()
        #         self.cap_esrExpectLab.deleteLater()
        #         self.cap_esrExpectLen.deleteLater()
        #         self.cap_esrExpectComboBox.deleteLater()
        #         # return
        #     case "Lnd":
        #         self.lnd_modeLab.deleteLater()
        #         self.lnd_volLab.deleteLater()
        #         self.lnd_volLen.deleteLater()
        #         self.lnd_volComboBox.deleteLater()
        #         self.lnd_freLab.deleteLater()
        #         self.lnd_freLen.deleteLater()
        #         self.lnd_freComboBox.deleteLater()
        #         self.lnd_testPurpose.deleteLater()
        #         self.lnd_testInstrument.deleteLater()
        #         self.lnd_testStep.deleteLater()
        #         self.lnd_lndExpectLab.deleteLater()
        #         self.lnd_lndExpectLen.deleteLater()
        #         self.lnd_lndExpectComboBox.deleteLater()
        #         self.lnd_qExpectLab.deleteLater()
        #         self.lnd_qExpectLen.deleteLater()
        #         # self.lnd_qExpectComboBox.deleteLater()
        #         # return
        #     case "Diode":
        #         self.diode_volLab.deleteLater()
        #         self.diode_volLen.deleteLater()
        #         self.diode_volComboBox.deleteLater()
        #         self.diode_currLab.deleteLater()
        #         self.diode_currLen.deleteLater()
        #         self.diode_currComboBox.deleteLater()
        #         self.diode_modeLab.deleteLater()
        #         self.diode_testPurpose.deleteLater()
        #         self.diode_testInstrument.deleteLater()
        #         self.diode_testStep.deleteLater()
        #         self.diode_volExpectLab.deleteLater()
        #         self.diode_volExpectLen.deleteLater()
        #         self.diode_volExpectComboBox.deleteLater()
        #         self.diode_currExpectLab.deleteLater()
        #         self.diode_currExpectLen.deleteLater()
        #         self.diode_currExpectComboBox.deleteLater()
        #         # return
        #     case "Mos":
        #         self.mos_volLab.deleteLater()
        #         self.mos_volLen.deleteLater()
        #         self.mos_volComboBox.deleteLater()
        #         self.mos_currLab.deleteLater()
        #         self.mos_currLen.deleteLater()
        #         self.mos_currComboBox.deleteLater()
        #         self.mos_modeLab.deleteLater()
        #         self.mos_testPurpose.deleteLater()
        #         self.mos_testInstrument.deleteLater()
        #         self.mos_testStep.deleteLater()
        #         self.mos_volExpectLab.deleteLater()
        #         self.mos_volExpectLen.deleteLater()
        #         self.mos_volExpectComboBox.deleteLater()
        #         self.mos_resExpectLab.deleteLater()
        #         self.mos_resExpectLen.deleteLater()
        #         self.mos_resExpectComboBox.deleteLater()
        #         # return

        # 设定测试模式
        self.test_Mode = "Bjt"


    # 场效应管测试参数UI配置
    def testMosConfig(self):
        # 提示信息
        self.statusBar().showMessage('场效应管测试模式')

        # 设定测参数默认值


        self.res_QGroupBox.close()
        self.res_resultQGroupBox.close()
        self.res_explainQGroupBox.close()
        self.cap_QGroupBox.close()
        self.cap_resultQGroupBox.close()
        self.cap_explainQGroupBox.close()
        self.lnd_QGroupBox.close()
        self.lnd_resultQGroupBox.close()
        self.lnd_explainQGroupBox.close()
        self.diode_QGroupBox.close()
        self.diode_resultQGroupBox.close()
        self.diode_explainQGroupBox.close()
        self.bjt_QGroupBox.close()
        self.bjt_resultQGroupBox.close()
        self.bjt_explainQGroupBox.close()

        self.mos_QGroupBox.show()
        self.mos_resultQGroupBox.show()
        self.mos_explainQGroupBox.show()
        # # 提示信息
        # self.statusBar().showMessage('场效应管测试模式')
        # self.mos_modeLab = QLabel("当前为场效应管测试模式", self)
        # self.mos_modeLab.setGeometry(60, 50, 200, 40)
        # self.mos_modeLab.show()

        # # 测试电压参数
        # self.mos_volLab = QLabel('测试电压：', self)
        # self.mos_volLab.setGeometry(60, 100, 80, 40)
        # self.mos_volLab.show()
        # self.mos_volLen = QLineEdit('请输入测试电压值', self)
        # self.mos_volLen.setValidator(
        #     QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.mos_volLen.setText("5")
        # self.testQThread.test_VoltageValue = 5
        # self.mos_volLen.setGeometry(160, 100, 80, 40)
        # self.mos_volLen.show()
        # self.mos_volComboBox = QComboBox(self)
        # self.mos_volComboBox.addItem("V")
        # self.mos_volComboBox.addItem("mV")
        # self.mos_volComboBox.setGeometry(260, 100, 80, 40)
        # self.mos_volComboBox.show()

        # # 测试电流参数
        # self.mos_currLab = QLabel('测试电流：', self)
        # self.mos_currLab.setGeometry(60, 150, 80, 40)
        # self.mos_currLab.show()
        # self.mos_currLen = QLineEdit('请输入测试电流值', self)
        # self.mos_currLen.setValidator(
        #     QRegExpValidator(QRegExp("[0-9]|10"), self))
        # # self.mos_currLen.setMaxLength(3)
        # self.mos_currLen.setText("1")
        # self.testQThread.test_CurrValue = 1
        # self.mos_currLen.setGeometry(160, 150, 80, 40)
        # self.mos_currLen.show()
        # self.mos_currComboBox = QComboBox(self)
        # self.mos_currComboBox.addItem("A")
        # self.mos_currComboBox.addItem("mA")
        # self.mos_currComboBox.setGeometry(260, 150, 80, 40)
        # self.mos_currComboBox.show()

        # # 导通电压期望值
        # self.mos_volExpectLab = QLabel('导通电压：', self)
        # self.mos_volExpectLab.setGeometry(60, 200, 80, 40)
        # self.mos_volExpectLab.show()
        # self.mos_volExpectLen = QLineEdit('请输入导通电压值', self)
        # self.mos_volExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # # self.mos_volExpectLen.setMaxLength(3)
        # self.testQThread.mos_VoltageExpect = 3
        # self.mos_volExpectLen.setText("{}".format(self.testQThread.mos_VoltageExpect))
        # self.mos_volExpectLen.setGeometry(160, 200, 80, 40)
        # self.mos_volExpectLen.show()
        # self.mos_volExpectComboBox = QComboBox(self)
        # self.mos_volExpectComboBox.addItem("V")
        # self.mos_volExpectComboBox.addItem("mV")
        # self.mos_volExpectComboBox.setGeometry(260, 200, 80, 40)
        # self.mos_volExpectComboBox.show()

        # # 导通电阻期望值
        # self.mos_resExpectLab = QLabel('导通电阻：', self)
        # self.mos_resExpectLab.setGeometry(60, 250, 80, 40)
        # self.mos_resExpectLab.show()
        # self.mos_resExpectLen = QLineEdit('请输入导通电阻值', self)
        # self.mos_resExpectLen.setValidator(
        #     QRegExpValidator(QRegExp("[0-9]|10"), self))
        # self.testQThread.mos_resExpect = 10
        # self.mos_resExpectLen.setText("{}".format(self.testQThread.mos_resExpect))
        # self.mos_resExpectLen.setGeometry(160, 250, 80, 40)
        # self.mos_resExpectLen.show()
        # self.mos_resExpectComboBox = QComboBox(self)
        # self.mos_resExpectComboBox.addItem("Ω")
        # self.mos_resExpectComboBox.addItem("mΩ")
        # self.mos_resExpectComboBox.setCurrentIndex(1)
        # self.mos_resExpectComboBox.setGeometry(260, 250, 80, 40)
        # self.mos_resExpectComboBox.show()

        # # 测试说明
        # self.mos_testPurpose = QLabel(self.mos_testPurposeData, self)
        # self.mos_testPurpose.setGeometry(60, 350, 200, 40)
        # self.mos_testPurpose.adjustSize()
        # self.mos_testPurpose.show()
        # self.mos_testInstrument = QLabel(self.mos_testInstrumentData, self)
        # self.mos_testInstrument.setGeometry(60, 380, 200, 40)
        # self.mos_testInstrument.adjustSize()
        # self.mos_testInstrument.show()
        # self.mos_testStep = QLabel(self.mos_testStepData, self)
        # self.mos_testStep.setGeometry(60, 410, 200, 40)
        # self.mos_testStep.adjustSize()
        # self.mos_testStep.show()

        # # 删除控件
        # match self.test_Mode:
        #     case "Res":
        #         self.res_modeLab.deleteLater()
        #         self.res_volLab.deleteLater()
        #         self.res_volLen.deleteLater()
        #         self.res_volComboBox.deleteLater()
        #         self.res_freLab.deleteLater()
        #         self.res_freLen.deleteLater()
        #         self.res_freComboBox.deleteLater()
        #         self.res_testPurpose.deleteLater()
        #         self.res_testInstrument.deleteLater()
        #         self.res_testStep.deleteLater()
        #         self.res_resExpectLab.deleteLater()
        #         self.res_resExpectLen.deleteLater()
        #         self.res_resExpectComboBox.deleteLater()
        #         # return
        #     case "Cap":
        #         self.cap_modeLab.deleteLater()
        #         self.cap_volLab.deleteLater()
        #         self.cap_volLen.deleteLater()
        #         self.cap_volComboBox.deleteLater()
        #         self.cap_freLab.deleteLater()
        #         self.cap_freLen.deleteLater()
        #         self.cap_freComboBox.deleteLater()
        #         self.cap_testPurpose.deleteLater()
        #         self.cap_testInstrument.deleteLater()
        #         self.cap_testStep.deleteLater()
        #         self.cap_capExpectLab.deleteLater()
        #         self.cap_capExpectLen.deleteLater()
        #         self.cap_capExpectComboBox.deleteLater()
        #         self.cap_esrExpectLab.deleteLater()
        #         self.cap_esrExpectLen.deleteLater()
        #         self.cap_esrExpectComboBox.deleteLater()
        #         # return
        #     case "Lnd":
        #         self.lnd_modeLab.deleteLater()
        #         self.lnd_volLab.deleteLater()
        #         self.lnd_volLen.deleteLater()
        #         self.lnd_volComboBox.deleteLater()
        #         self.lnd_freLab.deleteLater()
        #         self.lnd_freLen.deleteLater()
        #         self.lnd_freComboBox.deleteLater()
        #         self.lnd_testPurpose.deleteLater()
        #         self.lnd_testInstrument.deleteLater()
        #         self.lnd_testStep.deleteLater()
        #         self.lnd_lndExpectLab.deleteLater()
        #         self.lnd_lndExpectLen.deleteLater()
        #         self.lnd_lndExpectComboBox.deleteLater()
        #         self.lnd_qExpectLab.deleteLater()
        #         self.lnd_qExpectLen.deleteLater()
        #         # self.lnd_qExpectComboBox.deleteLater()
        #         # return
        #     case "Diode":
        #         self.diode_volLab.deleteLater()
        #         self.diode_volLen.deleteLater()
        #         self.diode_volComboBox.deleteLater()
        #         self.diode_currLab.deleteLater()
        #         self.diode_currLen.deleteLater()
        #         self.diode_currComboBox.deleteLater()
        #         self.diode_modeLab.deleteLater()
        #         self.diode_testPurpose.deleteLater()
        #         self.diode_testInstrument.deleteLater()
        #         self.diode_testStep.deleteLater()
        #         self.diode_volExpectLab.deleteLater()
        #         self.diode_volExpectLen.deleteLater()
        #         self.diode_volExpectComboBox.deleteLater()
        #         self.diode_currExpectLab.deleteLater()
        #         self.diode_currExpectLen.deleteLater()
        #         self.diode_currExpectComboBox.deleteLater()
        #         # return
        #     case "Bjt":
        #         self.bjt_volLab.deleteLater()
        #         self.bjt_volLen.deleteLater()
        #         self.bjt_volComboBox.deleteLater()
        #         self.bjt_currLab.deleteLater()
        #         self.bjt_currLen.deleteLater()
        #         self.bjt_currComboBox.deleteLater()
        #         self.bjt_modeLab.deleteLater()
        #         self.bjt_testPurpose.deleteLater()
        #         self.bjt_testInstrument.deleteLater()
        #         self.bjt_testStep.deleteLater()
        #         self.bjt_volExpectLab.deleteLater()
        #         self.bjt_volExpectLen.deleteLater()
        #         self.bjt_volExpectComboBox.deleteLater()
        #         self.bjt_currExpectLab.deleteLater()
        #         self.bjt_currExpectLen.deleteLater()
        #         self.bjt_currExpectComboBox.deleteLater()
        #         self.bjt_betaExpectLab.deleteLater()
        #         self.bjt_betaExpectLen.deleteLater()
        #         # self.bjt_betaExpectComboBox.deleteLater()
        #         # return

        # 设定测试模式
        self.test_Mode = "Mos"


# 开始测试后弹窗提示
class TestWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 70)
        self.setWindowTitle("测试状态")
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 去掉标题栏的代码
        self.windowShow()

    def windowShow(self):

        # 展示内容
        self.label = QLabel("正在测试请稍等...", self)
        self.stopTestBtn = QPushButton("停止测试", self)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        # 子窗口中的布局
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.stopTestBtn, 0, 1)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)


    ex = UIViewClass()

    sys.exit(app.exec_())
