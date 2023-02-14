#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.realpath("."))

from PyQt5.QtWidgets import *  # QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu, QInputDialog, QLineEdit, QLabel, QComboBox
from PyQt5.QtGui import *  # QFont, QDoubleValidator, QIcon
from PyQt5.QtCore import *  # QCoreApplication

from pyqtgraph import GraphicsLayoutWidget
# import pyqtgraph as pg
# import numpy as np
# import pyqtgraph.exporters as pe
# import qdarkstyle, requests, time, random, json, datetime, re
# from qt_material import apply_stylesheet

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
        # 初始化所有UI测试项目
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
        self.reportOutMenu = QAction('导出测试数据', self)
        # fileMenu.addAction(self.impIn)
        fileMenu.addAction(self.reportOutMenu)

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
        self.impMes = QAction("关于器件自动化测试工具", self)
        messageMenu.addAction(self.impMes)

        # 配置主窗口布局
        self.mainWidget()

        # 开始按钮
        self.btn = QPushButton('开始测试', self)
        self.btn.setToolTip('点击开始器件测试')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(780, 480)

        # 退出按钮
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(920, 480)

        # 窗口和标题并创建所有控件
        self.setGeometry(580, 270, 1024, 576)
        self.center()
        self.setWindowTitle('器件自动化测试')
        self.setWindowIcon(QIcon(r'D:\Data\Project\Python\ExcelATE_V2\Gui\UIView\favicon.ico'))
        self.setFixedSize(self.width(), self.height())  # 固定窗口大小和关闭最大化
        self.show()

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

    # 配置主窗口布局
    def mainWidget(self):
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.res_QGroupBox, 2, 0)
        mainLayout.addWidget(self.res_resultQGroupBox, 2, 1)
        mainLayout.addWidget(self.res_explainQGroupBox, 1, 0, 1, 2)

        mainLayout.addWidget(self.cap_QGroupBox, 2, 0)
        mainLayout.addWidget(self.cap_resultQGroupBox, 2, 1)
        mainLayout.addWidget(self.cap_explainQGroupBox, 1, 0, 1, 2)

        mainLayout.addWidget(self.lnd_QGroupBox, 2, 0)
        mainLayout.addWidget(self.lnd_resultQGroupBox, 2, 1)
        mainLayout.addWidget(self.lnd_explainQGroupBox, 1, 0, 1, 2)

        mainLayout.addWidget(self.diode_QGroupBox, 2, 0)
        mainLayout.addWidget(self.diode_resultQGroupBox, 2, 1)
        mainLayout.addWidget(self.diode_explainQGroupBox, 1, 0, 1, 2)

        mainLayout.addWidget(self.bjt_QGroupBox, 2, 0)
        mainLayout.addWidget(self.bjt_resultQGroupBox, 2, 1)
        mainLayout.addWidget(self.bjt_explainQGroupBox, 1, 0, 1, 2)

        mainLayout.addWidget(self.mos_QGroupBox, 2, 0)
        mainLayout.addWidget(self.mos_resultQGroupBox, 2, 1)
        mainLayout.addWidget(self.mos_explainQGroupBox, 1, 0, 1, 2)

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
        cp = QDesktopWidget().availableGeometry().center(
        )  # 获取显示器的分辨率，然后得到屏幕中间点的位置
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

    # 电阻测试UI初始化
    def res_testInitConfig(self):
        self.res_QGroupBox = QGroupBox("测试参数")
        self.res_resultQGroupBox = QGroupBox("测试结果")
        self.res_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QVBoxLayout()
        explainLayout = QVBoxLayout()

        self.res_modeLab = QLabel("当前为电阻测试模式", self)

        # 测试值
        self.res_volLab = QLabel('测试电压：', self)
        self.res_volLen = QLineEdit('请输入测试电压值', self)
        self.res_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),
                                                      self))  # 按照正则表达式设定可输入的内容
        self.testQThread.test_VoltageValue = 1
        self.res_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
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

        # 期望值
        self.res_resExpectLab = QLabel('电阻期望值：', self)
        self.res_resExpectLen = QLineEdit('请输入电阻期望值', self)
        self.res_resExpectLen.setMaxLength(3)
        self.testQThread.res_resExpect = 100
        self.res_resExpectLen.setText("{}".format(
            self.testQThread.res_resExpect))
        self.res_resExpectComboBox = QComboBox(self)
        self.res_resExpectComboBox.addItem("MΩ")
        self.res_resExpectComboBox.addItem("kΩ")
        self.res_resExpectComboBox.addItem("Ω")
        self.res_resExpectComboBox.addItem("mΩ")
        self.res_resExpectComboBox.setCurrentIndex(2)  # 设置默认单位值

        # 结果值
        self.res_resResultLab = QLabel('电阻值测试结果：', self)

        # 测试说明
        self.res_testPurpose = QLabel(self.res_testPurposeData, self)
        self.res_testInstrument = QLabel(self.res_testInstrumentData, self)
        self.res_testStep = QLabel(self.res_testStepData, self)

        layout.addWidget(self.res_modeLab, 1, 0)
        layout.addWidget(self.res_volLab, 2, 0)
        layout.addWidget(self.res_volLen, 2, 1)
        layout.addWidget(self.res_volComboBox, 2, 2)
        layout.addWidget(self.res_freLab)
        layout.addWidget(self.res_freLen)
        layout.addWidget(self.res_freComboBox)
        layout.addWidget(self.res_resExpectLab)
        layout.addWidget(self.res_resExpectLen)
        layout.addWidget(self.res_resExpectComboBox)

        resultLayout.addWidget(self.res_resResultLab)
        resultLayout.addStretch(1)

        explainLayout.addWidget(self.res_testPurpose)
        explainLayout.addWidget(self.res_testInstrument)
        explainLayout.addWidget(self.res_testStep)
        explainLayout.addStretch(1)

        self.res_QGroupBox.setLayout(layout)
        self.res_resultQGroupBox.setLayout(resultLayout)
        self.res_explainQGroupBox.setLayout(explainLayout)

    # 电容测试UI初始化
    def cap_testInitConfig(self):
        self.cap_QGroupBox = QGroupBox("测试参数")
        self.cap_resultQGroupBox = QGroupBox("测试结果")
        self.cap_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QVBoxLayout()
        explainLayout = QVBoxLayout()

        self.cap_modeLab = QLabel("当前为电容测试模式", self)

        # 测试值
        self.cap_volLab = QLabel('测试电压：', self)
        self.cap_volLen = QLineEdit('请输入测试电压值', self)
        self.cap_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),
                                                      self))  # 按照正则表达式设定可输入的内容
        self.testQThread.test_VoltageValue = 1
        self.cap_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
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

        # 期望值
        self.cap_capExpectLab = QLabel('电容期望值：', self)
        self.cap_capExpectLen = QLineEdit('请输入电容期望值', self)
        self.cap_capExpectLen.setMaxLength(3)
        self.testQThread.cap_capExpect = 100
        self.cap_capExpectLen.setText("{}".format(
            self.testQThread.cap_capExpect))
        self.cap_capExpectComboBox = QComboBox(self)
        self.cap_capExpectComboBox.addItem("F")
        self.cap_capExpectComboBox.addItem("mF")
        self.cap_capExpectComboBox.addItem("uF")
        self.cap_capExpectComboBox.addItem("nF")
        self.cap_capExpectComboBox.addItem("pF")
        self.cap_capExpectComboBox.setCurrentIndex(2)

        self.cap_esrExpectLab = QLabel('等效串联电阻期望值：', self)
        self.cap_esrExpectLen = QLineEdit('请输入等效串联电阻期望值', self)
        self.cap_esrExpectLen.setMaxLength(3)
        self.testQThread.cap_esrExpect = 100
        self.cap_esrExpectLen.setText("{}".format(
            self.testQThread.cap_esrExpect))
        self.cap_esrExpectComboBox = QComboBox(self)
        self.cap_esrExpectComboBox.addItem("kΩ")
        self.cap_esrExpectComboBox.addItem("Ω")
        self.cap_esrExpectComboBox.addItem("mΩ")
        self.cap_esrExpectComboBox.setCurrentIndex(1)

        # 结果值
        self.cap_capResultLab = QLabel('电容测试结果：', self)
        self.cap_esrResultLab = QLabel('等效串联电阻测试结果：', self)

        self.cap_testPurpose = QLabel(self.cap_testPurposeData, self)
        self.cap_testInstrument = QLabel(self.cap_testInstrumentData, self)
        self.cap_testStep = QLabel(self.cap_testStepData, self)

        layout.addWidget(self.cap_modeLab, 1, 0)
        layout.addWidget(self.cap_volLab, 2, 0)
        layout.addWidget(self.cap_volLen, 2, 1)
        layout.addWidget(self.cap_volComboBox, 2, 2)
        layout.addWidget(self.cap_freLab)
        layout.addWidget(self.cap_freLen)
        layout.addWidget(self.cap_freComboBox)
        layout.addWidget(self.cap_capExpectLab)
        layout.addWidget(self.cap_capExpectLen)
        layout.addWidget(self.cap_capExpectComboBox)
        layout.addWidget(self.cap_esrExpectLab)
        layout.addWidget(self.cap_esrExpectLen)
        layout.addWidget(self.cap_esrExpectComboBox)

        resultLayout.addWidget(self.cap_capResultLab)
        resultLayout.addWidget(self.cap_esrResultLab)
        resultLayout.addStretch(1)

        explainLayout.addWidget(self.cap_testPurpose)
        explainLayout.addWidget(self.cap_testInstrument)
        explainLayout.addWidget(self.cap_testStep)
        explainLayout.addStretch(1)

        self.cap_QGroupBox.setLayout(layout)
        self.cap_resultQGroupBox.setLayout(resultLayout)
        self.cap_explainQGroupBox.setLayout(explainLayout)

    # 电感测试UI初始化
    def lnd_testInitConfig(self):
        self.lnd_QGroupBox = QGroupBox("测试参数")
        self.lnd_resultQGroupBox = QGroupBox("测试结果")
        self.lnd_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QVBoxLayout()
        explainLayout = QVBoxLayout()

        self.lnd_modeLab = QLabel("当前为电感测试模式", self)

        # 测试值
        self.lnd_volLab = QLabel('测试电压：', self)
        self.lnd_volLen = QLineEdit('请输入测试电压值', self)
        self.lnd_volLen.setValidator(QRegExpValidator(QRegExp("[0-1]"),
                                                      self))  # 按照正则表达式设定可输入的内容
        self.testQThread.test_VoltageValue = 1
        self.lnd_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
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

        # 期望值
        self.lnd_lndExpectLab = QLabel('电感期望值：', self)
        self.lnd_lndExpectLen = QLineEdit('请输入电感期望值', self)
        self.lnd_lndExpectLen.setMaxLength(3)
        self.testQThread.lnd_lndExpect = 100
        self.lnd_lndExpectLen.setText("{}".format(
            self.testQThread.lnd_lndExpect))
        self.lnd_lndExpectComboBox = QComboBox(self)
        self.lnd_lndExpectComboBox.addItem("Hz")
        self.lnd_lndExpectComboBox.addItem("kHz")

        self.lnd_qExpectLab = QLabel('品质因数期望值：', self)
        self.lnd_qExpectLen = QLineEdit('请输入品质因数期望值', self)
        self.lnd_qExpectLen.setMaxLength(3)
        self.testQThread.lnd_qExpect = 100
        self.lnd_qExpectLen.setText("{}".format(self.testQThread.lnd_qExpect))
        # self.lnd_qExpectComboBox = QComboBox(self)

        # 结果值
        self.lnd_lndResultLab = QLabel('电感测试结果：', self)
        self.lnd_qResultLab = QLabel('品质因数测试结果：', self)

        # 测试说明
        self.lnd_testPurpose = QLabel(self.lnd_testPurposeData, self)
        self.lnd_testInstrument = QLabel(self.lnd_testInstrumentData, self)
        self.lnd_testStep = QLabel(self.lnd_testStepData, self)

        layout.addWidget(self.lnd_modeLab, 1, 0)
        layout.addWidget(self.lnd_volLab, 2, 0)
        layout.addWidget(self.lnd_volLen, 2, 1)
        layout.addWidget(self.lnd_volComboBox, 2, 2)
        layout.addWidget(self.lnd_freLab)
        layout.addWidget(self.lnd_freLen)
        layout.addWidget(self.lnd_freComboBox)
        layout.addWidget(self.lnd_lndExpectLab)
        layout.addWidget(self.lnd_lndExpectLen)
        layout.addWidget(self.lnd_lndExpectComboBox)
        layout.addWidget(self.lnd_qExpectLab)
        layout.addWidget(self.lnd_qExpectLen)
        # layout.addWidget(self.lnd_qExpectComboBox)

        resultLayout.addWidget(self.lnd_lndResultLab)
        resultLayout.addWidget(self.lnd_qResultLab)
        resultLayout.addStretch(1)

        explainLayout.addWidget(self.lnd_testPurpose)
        explainLayout.addWidget(self.lnd_testInstrument)
        explainLayout.addWidget(self.lnd_testStep)
        explainLayout.addStretch(1)

        self.lnd_QGroupBox.setLayout(layout)
        self.lnd_resultQGroupBox.setLayout(resultLayout)
        self.lnd_explainQGroupBox.setLayout(explainLayout)

    # 二极管测试UI初始化
    def diode_testInitConfig(self):
        self.diode_QGroupBox = QGroupBox("测试参数")
        self.diode_resultQGroupBox = QGroupBox("测试结果")
        self.diode_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QVBoxLayout()
        explainLayout = QVBoxLayout()

        self.testQThread.test_Mode = "Diode"
        self.diode_modeLab = QLabel("当前为二极管测试模式", self)

        # 测试值
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
        self.diode_currLen.setText("{}".format(
            self.testQThread.test_CurrValue))
        self.diode_currComboBox = QComboBox(self)
        self.diode_currComboBox.addItem("A")
        self.diode_currComboBox.addItem("mA")

        # 期望值
        self.diode_volExpectLab = QLabel('导通电压期望值：', self)
        self.diode_volExpectLen = QLineEdit('请输入导通电压期望值', self)
        self.diode_volExpectLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.diode_volExpectLen.setMaxLength(3)
        self.testQThread.diode_VoltageExpect = 3
        self.diode_volExpectLen.setText("{}".format(
            self.testQThread.diode_VoltageExpect))
        self.diode_volExpectComboBox = QComboBox(self)
        self.diode_volExpectComboBox.addItem("V")
        self.diode_volExpectComboBox.addItem("mV")

        self.diode_currExpectLab = QLabel('漏电流期望值：', self)
        self.diode_currExpectLen = QLineEdit('请输入漏电流期望值', self)
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

        # 测试结果
        self.diode_volResultLab = QLabel("导通电压测试结果：", self)
        self.diode_currResultLab = QLabel("漏电流测试结果：", self)

        self.diode_testPurpose = QLabel(self.diode_testPurposeData, self)
        self.diode_testInstrument = QLabel(self.diode_testInstrumentData, self)
        self.diode_testStep = QLabel(self.diode_testStepData, self)

        layout.addWidget(self.diode_modeLab, 1, 0)
        layout.addWidget(self.diode_volLab, 2, 0)
        layout.addWidget(self.diode_volLen, 2, 1)
        layout.addWidget(self.diode_volComboBox, 2, 2)
        layout.addWidget(self.diode_currLab)
        layout.addWidget(self.diode_currLen)
        layout.addWidget(self.diode_currComboBox)
        layout.addWidget(self.diode_volExpectLab)
        layout.addWidget(self.diode_volExpectLen)
        layout.addWidget(self.diode_volExpectComboBox)
        layout.addWidget(self.diode_currExpectLab)
        layout.addWidget(self.diode_currExpectLen)
        layout.addWidget(self.diode_currExpectComboBox)

        resultLayout.addWidget(self.diode_volResultLab)
        resultLayout.addWidget(self.diode_currResultLab)
        resultLayout.addStretch(1)

        explainLayout.addWidget(self.diode_testPurpose)
        explainLayout.addWidget(self.diode_testInstrument)
        explainLayout.addWidget(self.diode_testStep)
        explainLayout.addStretch(1)

        self.diode_QGroupBox.setLayout(layout)
        self.diode_resultQGroupBox.setLayout(resultLayout)
        self.diode_explainQGroupBox.setLayout(explainLayout)

    # 三极管测试UI初始化
    def bjt_testInitConfig(self):
        self.bjt_QGroupBox = QGroupBox("测试参数")
        self.bjt_resultQGroupBox = QGroupBox("测试结果")
        self.bjt_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QVBoxLayout()
        explainLayout = QVBoxLayout()

        # 提示信息
        self.bjt_modeLab = QLabel("当前为三极管测试模式", self)

        # 测试值
        self.bjt_volLab = QLabel('测试电压：', self)
        self.bjt_volLen = QLineEdit('请输入测试电压值', self)
        self.bjt_volLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.test_VoltageValue = 5
        self.bjt_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.bjt_volComboBox = QComboBox(self)
        self.bjt_volComboBox.addItem("V")
        self.bjt_volComboBox.addItem("mV")

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

        # 期望值
        self.bjt_volExpectLab = QLabel('导通电压期望值：', self)
        self.bjt_volExpectLen = QLineEdit('请输入导通电压期望值', self)
        self.bjt_volExpectLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.bjt_VoltageExpect = 3
        self.bjt_volExpectLen.setText("{}".format(
            self.testQThread.bjt_VoltageExpect))
        self.bjt_volExpectComboBox = QComboBox(self)
        self.bjt_volExpectComboBox.addItem("V")
        self.bjt_volExpectComboBox.addItem("mV")

        self.bjt_currExpectLab = QLabel('集电极电流i-c期望值：', self)
        self.bjt_currExpectLen = QLineEdit('请输入集电极电流i-c期望值', self)
        self.bjt_currExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.bjt_currExpect = 10
        self.bjt_currExpectLen.setText("{}".format(
            self.testQThread.bjt_currExpect))
        self.bjt_currExpectComboBox = QComboBox(self)
        self.bjt_currExpectComboBox.addItem("A")
        self.bjt_currExpectComboBox.addItem("mA")
        self.bjt_currExpectComboBox.addItem("uA")
        self.bjt_currExpectComboBox.setCurrentIndex(1)

        self.bjt_betaExpectLab = QLabel('放大倍数β期望值：', self)
        self.bjt_betaExpectLen = QLineEdit('请输入放大倍数β期望值', self)
        self.bjt_betaExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.bjt_betaExpect = 300
        self.bjt_betaExpectLen.setText("{}".format(
            self.testQThread.bjt_betaExpect))
        # self.bjt_betaExpectComboBox = QComboBox(self)

        # 测试结果
        self.bjt_volResultLab = QLabel('导通电压测试结果：', self)
        self.bjt_currResultLab = QLabel('集电极电流i-c测试结果：', self)
        self.bjt_betaResultLab = QLabel('放大倍数β测试结果：', self)

        # 测试说明
        self.bjt_testPurpose = QLabel(self.bjt_testPurposeData, self)
        self.bjt_testInstrument = QLabel(self.bjt_testInstrumentData, self)
        self.bjt_testStep = QLabel(self.bjt_testStepData, self)

        layout.addWidget(self.bjt_modeLab, 1, 0)
        layout.addWidget(self.bjt_volLab, 2, 0)
        layout.addWidget(self.bjt_volLen, 2, 1)
        layout.addWidget(self.bjt_volComboBox, 2, 2)
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

        resultLayout.addWidget(self.bjt_volResultLab)
        resultLayout.addWidget(self.bjt_currResultLab)
        resultLayout.addWidget(self.bjt_betaResultLab)
        resultLayout.addStretch(1)

        explainLayout.addWidget(self.bjt_testPurpose)
        explainLayout.addWidget(self.bjt_testInstrument)
        explainLayout.addWidget(self.bjt_testStep)
        explainLayout.addStretch(1)

        self.bjt_QGroupBox.setLayout(layout)
        self.bjt_resultQGroupBox.setLayout(resultLayout)
        self.bjt_explainQGroupBox.setLayout(explainLayout)

    # 场效应管测试UI初始化
    def mos_testInitConfig(self):
        self.mos_QGroupBox = QGroupBox("测试参数")
        self.mos_resultQGroupBox = QGroupBox("测试结果")
        self.mos_explainQGroupBox = QGroupBox("测试说明")
        layout = QGridLayout()
        resultLayout = QVBoxLayout()
        explainLayout = QVBoxLayout()

        # 提示信息
        self.mos_modeLab = QLabel("当前为场效应管测试模式", self)

        # 测试值
        self.mos_volLab = QLabel('测试电压：', self)
        self.mos_volLen = QLineEdit('请输入测试电压值', self)
        self.mos_volLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        self.testQThread.test_VoltageValue = 5
        self.mos_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.mos_volComboBox = QComboBox(self)
        self.mos_volComboBox.addItem("V")
        self.mos_volComboBox.addItem("mV")

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

        # 期望值
        self.mos_volExpectLab = QLabel('导通电压期望值：', self)
        self.mos_volExpectLen = QLineEdit('请输入导通电压期望值', self)
        self.mos_volExpectLen.setValidator(
            QRegExpValidator(QRegExp("^((\d{1,2})|(1[0-4]\d)|(150))$"), self))
        # self.mos_volExpectLen.setMaxLength(3)
        self.testQThread.mos_VoltageExpect = 3
        self.mos_volExpectLen.setText("{}".format(
            self.testQThread.mos_VoltageExpect))
        self.mos_volExpectComboBox = QComboBox(self)
        self.mos_volExpectComboBox.addItem("V")
        self.mos_volExpectComboBox.addItem("mV")

        self.mos_resExpectLab = QLabel('导通电阻期望值：', self)
        self.mos_resExpectLen = QLineEdit('请输入导通电阻期望值', self)
        self.mos_resExpectLen.setValidator(
            QRegExpValidator(QRegExp("[0-9]|10"), self))
        self.testQThread.mos_resExpect = 10
        self.mos_resExpectLen.setText("{}".format(
            self.testQThread.mos_resExpect))
        self.mos_resExpectComboBox = QComboBox(self)
        self.mos_resExpectComboBox.addItem("Ω")
        self.mos_resExpectComboBox.addItem("mΩ")

        # 测试结果
        self.mos_volResultLab = QLabel('导通电压测试结果：', self)
        self.mos_resResultLab = QLabel('导通电阻测试结果：', self)

        # 测试说明
        self.mos_testPurpose = QLabel(self.mos_testPurposeData, self)
        self.mos_testInstrument = QLabel(self.mos_testInstrumentData, self)
        self.mos_testStep = QLabel(self.mos_testStepData, self)

        layout.addWidget(self.mos_modeLab, 1, 0)
        layout.addWidget(self.mos_volLab, 2, 0)
        layout.addWidget(self.mos_volLen, 2, 1)
        layout.addWidget(self.mos_volComboBox, 2, 2)
        layout.addWidget(self.mos_currLab)
        layout.addWidget(self.mos_currLen)
        layout.addWidget(self.mos_currComboBox)
        layout.addWidget(self.mos_volExpectLab)
        layout.addWidget(self.mos_volExpectLen)
        layout.addWidget(self.mos_volExpectComboBox)
        layout.addWidget(self.mos_resExpectLab)
        layout.addWidget(self.mos_resExpectLen)
        layout.addWidget(self.mos_resExpectComboBox)

        resultLayout.addWidget(self.mos_volResultLab)
        resultLayout.addWidget(self.mos_resResultLab)
        resultLayout.addStretch(1)

        explainLayout.addWidget(self.mos_testPurpose)
        explainLayout.addWidget(self.mos_testInstrument)
        explainLayout.addWidget(self.mos_testStep)
        explainLayout.addStretch(1)

        self.mos_QGroupBox.setLayout(layout)
        self.mos_resultQGroupBox.setLayout(resultLayout)
        self.mos_explainQGroupBox.setLayout(explainLayout)

    # 电阻测试参数UI配置
    def testResConfig(self):
        # 提示信息
        self.statusBar().showMessage('电阻测试模式')
        # 设定测试参数默认值
        self.testQThread.test_VoltageValue = 1
        self.res_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.testQThread.test_freValue = 100
        self.res_freLen.setText("{}".format(self.testQThread.test_freValue))
        self.testQThread.res_resExpect = 100
        self.res_resExpectLen.setText("{}".format(
            self.testQThread.res_resExpect))
        # 设定测试模式
        self.testQThread.test_Mode = "Res"

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

    # 电容测试参数UI配置
    def testCapConfig(self):
        # 提示信息
        self.statusBar().showMessage('电容测试模式')
        # 设定测试参数默认值
        self.testQThread.test_VoltageValue = 1
        self.cap_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.testQThread.test_freValue = 100
        self.cap_freLen.setText("{}".format(self.testQThread.test_freValue))
        self.testQThread.cap_capExpect = 100
        self.cap_capExpectLen.setText("{}".format(
            self.testQThread.cap_capExpect))
        self.testQThread.cap_esrExpect = 100
        self.cap_esrExpectLen.setText("{}".format(
            self.testQThread.cap_esrExpect))
        # 设定测试模式
        self.testQThread.test_Mode = "Cap"

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

    # 电感测试参数UI配置
    def testLndConfig(self):
        # 提示信息
        self.statusBar().showMessage('电感测试模式')
        # 设定测试参数默认值
        self.testQThread.test_VoltageValue = 1
        self.lnd_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.testQThread.test_freValue = 100
        self.lnd_freLen.setText("{}".format(self.testQThread.test_freValue))
        self.testQThread.lnd_lndExpect = 100
        self.lnd_lndExpectLen.setText("{}".format(
            self.testQThread.lnd_lndExpect))
        self.testQThread.lnd_qExpect = 100
        self.lnd_qExpectLen.setText("{}".format(self.testQThread.lnd_qExpect))
        # 设定测试模式
        self.testQThread.test_Mode = "Lnd"

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

    # 二极管测试参数UI配置
    def testDiodeConfig(self):
        # 提示信息
        self.statusBar().showMessage('二极管测试模式')
        # 设定测试参数默认值
        self.testQThread.test_VoltageValue = 1
        self.diode_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.testQThread.test_CurrValue = 1
        self.diode_currLen.setText("{}".format(
            self.testQThread.test_CurrValue))
        self.testQThread.diode_VoltageExpect = 3
        self.diode_volExpectLen.setText("{}".format(
            self.testQThread.diode_VoltageExpect))
        self.testQThread.diode_currExpect = 10
        self.diode_currExpectLen.setText("{}".format(
            self.testQThread.diode_currExpect))
        # 设定测试模式
        self.testQThread.test_Mode = "Diode"

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

    # 三极管测试参数UI配置
    def testBjtConfig(self):
        # 提示信息
        self.statusBar().showMessage('三极管测试模式')
        # 设定测试参数默认值
        self.testQThread.test_VoltageValue = 5
        self.bjt_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.testQThread.test_CurrValue = 1
        self.bjt_currLen.setText("{}".format(self.testQThread.test_CurrValue))
        self.testQThread.bjt_VoltageExpect = 3
        self.bjt_volExpectLen.setText("{}".format(
            self.testQThread.bjt_VoltageExpect))
        self.testQThread.bjt_currExpect = 10
        self.bjt_currExpectLen.setText("{}".format(
            self.testQThread.bjt_currExpect))
        self.testQThread.bjt_betaExpect = 300
        self.bjt_betaExpectLen.setText("{}".format(
            self.testQThread.bjt_betaExpect))
        # 设定测试模式
        self.testQThread.test_Mode = "Bjt"

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

    # 场效应管测试参数UI配置
    def testMosConfig(self):
        # 提示信息
        self.statusBar().showMessage('场效应管测试模式')
        # 设定测参数默认值
        self.testQThread.test_VoltageValue = 5
        self.mos_volLen.setText("{}".format(
            self.testQThread.test_VoltageValue))
        self.testQThread.test_CurrValue = 1
        self.mos_currLen.setText("{}".format(self.testQThread.test_CurrValue))
        self.testQThread.mos_VoltageExpect = 3
        self.mos_volExpectLen.setText("{}".format(
            self.testQThread.mos_VoltageExpect))
        self.testQThread.mos_resExpect = 10
        self.mos_resExpectLen.setText("{}".format(
            self.testQThread.mos_resExpect))
        # 设定测试模式
        self.testQThread.test_Mode = "Mos"

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


# 开始测试后弹窗提示
class TestWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 70)
        self.setWindowTitle("测试状态")
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 去掉标题栏
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

