#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.realpath("."))

import time

from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu, QInputDialog, QLineEdit, QLabel, QComboBox
from PyQt5.QtGui import QFont, QDoubleValidator
from PyQt5.QtCore import QCoreApplication

# import Diode
from Material import Diode


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.testInitConfig()
        self.initUI()
        self.test_VoltageValue = None
        self.test_Mode = None

    def initUI(self):
        # QToolTip.setFont(QFont('SansSerif', 10))    # 设定主窗口字体和大小
        # self.setToolTip('点击开始测试') # 主窗口鼠标悬停提示信息

        # 状态栏信息
        self.statusBar().showMessage('请设定测试参数')

        # 配置一级菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        testMenu = menubar.addMenu('测试')
        # impMenu = QAction('&测试类型',self)
        # impMenu2 = QAction('测试类型2', self)
        # impMenu.addAction(impDiode)
        # impMenu.addAction(impCap)

        # 配置文件菜单
        impIn = QAction('导入测试模板', self)
        impOut = QAction('导出测试数据', self)
        fileMenu.addAction(impIn)
        fileMenu.addAction(impOut)

        # 配置测试菜单
        impRes = QAction('电阻测试', self)
        impCap = QAction('电容测试', self)
        impInd = QAction('电感测试', self)
        impDiode = QAction('二极管测试', self)
        impBJT = QAction('三极管测试', self)
        impMos = QAction('场效应管测试', self)
        testMenu.addAction(impRes)
        testMenu.addAction(impCap)
        testMenu.addAction(impInd)
        testMenu.addAction(impDiode)
        testMenu.addAction(impBJT)
        testMenu.addAction(impMos)

        # 菜单触发事件
        impDiode.triggered.connect(self.testDiodeConfig)
        impCap.triggered.connect(self.testCapConfig)

        # 开始按钮
        btn = QPushButton('开始测试', self)
        btn.setToolTip('点击开始器件测试')
        btn.clicked.connect(self.test)  # 点击开始测试按钮调用test函数
        btn.resize(btn.sizeHint())
        btn.move(500, 500)

        # 退出按钮
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(1000, 600)

        # 窗口和标题并创建所有控件
        self.setGeometry(580, 270, 1280, 720)
        self.center()
        self.setWindowTitle('器件自动化测试')
        self.show()


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

    # 电容测试参数配置
    def testCapConfig(self):
        if self.test_Mode == "Cap":
            pass
        else:
            self.cap_volLab = QLabel('测试电压：', self)
            self.cap_volLen = QLineEdit('请输入测试电压值', self)
            self.cap_comboBoxVol = QComboBox(self)
            self.cap_comboBoxVol.addItem("V")
            self.cap_comboBoxVol.addItem("mV")
            self.cap_volLen.setMaxLength(2)
            self.cap_volLen.setText("5")
            self.test_VoltageValue = 5
            self.cap_volLab.setGeometry(100, 200, 80, 40)
            self.cap_volLen.setGeometry(200, 200, 80, 40)
            self.cap_comboBoxVol.setGeometry(300, 200, 80, 40)
            self.cap_volLab.show()
            self.cap_volLen.show()
            self.cap_comboBoxVol.show()
            self.diode_volLab.deleteLater()
            self.diode_volLen.deleteLater()
            self.diode_comboBoxVol.deleteLater()
            self.test_Mode = "Cap"
        self.cap_volLen.textChanged.connect(self.testCapVol)

    def testCapVol(self, test_VoltageValue):
        self.test_VoltageValue = test_VoltageValue

    # def testCapVol(self):
    #     self.test_VoltageValue, ok = QInputDialog.getText(self, '测试电压', '请输入测试电压:')
    #     if ok:
    #         self.cap_volLen.setText('测试电压为:{} V'.format(self.test_VoltageValue))

    # 二极管测试参数配置
    def testDiodeConfig(self):
        if self.test_Mode == "Diode":
            pass
        else:
            self.diode_volLab = QLabel('测试电压：', self)
            self.diode_volLen = QLineEdit('请输入测试电压值', self)
            self.diode_comboBoxVol = QComboBox(self)
            self.diode_comboBoxVol.addItem("V")
            self.diode_comboBoxVol.addItem("mV")
            self.diode_volLen.setMaxLength(2)
            self.diode_volLen.setText("5")
            self.test_VoltageValue = 5
            self.diode_volLab.setGeometry(100, 300, 80, 40)
            self.diode_volLen.setGeometry(200, 300, 80, 40)
            self.diode_comboBoxVol.setGeometry(300, 300, 80, 40)
            self.diode_volLab.show()
            self.diode_volLen.show()
            self.diode_comboBoxVol.show()
            self.cap_volLab.deleteLater()
            self.cap_volLen.deleteLater()
            self.cap_comboBoxVol.deleteLater()
            self.test_Mode = "Diode"
        # self.diode_volLab.clicked.connect(self.testDiodeVol)
        self.diode_volLen.textChanged[str].connect(self.testDiodeVol)

    def testDiodeVol(self, test_VoltageValue):
        self.test_VoltageValue = test_VoltageValue

    # def testDiodeVol(self):
    #     self.test_VoltageValue,ok=QInputDialog.getText(self,'测试电压','请输入测试电压:')
    #     if ok:
    #         self.diode_volLen.setText('测试电压为:{} V'.format(self.test_VoltageValue))

    # 测试状态提示
    def test(self):
        self.statusBar().showMessage('正在测试')
        reply = QMessageBox.question(self, '提示', '请确认是否进行测试',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            print(self.test_VoltageValue)
            print(self.cap_comboBoxVol)
            Diode.main(self.test_VoltageValue)
            self.statusBar().showMessage('完成测试')
            QMessageBox.information(self, '提示', '完成测试')
        else:
            self.statusBar().showMessage('取消测试')

    # 初始化所有测试项目
    def testInitConfig(self):
        self.cap_volLab = QLabel('测试电压：', self)
        self.cap_volLen = QLineEdit('请输入测试电压值', self)
        self.cap_comboBoxVol = QComboBox(self)
        self.diode_volLab = QLabel('测试电压：', self)
        self.diode_volLen = QLineEdit('请输入测试电压值', self)
        self.diode_comboBoxVol = QComboBox(self)
        self.cap_volLab.setGeometry(100, 200, 80, 40)
        self.cap_volLen.setGeometry(200, 200, 80, 40)
        self.cap_comboBoxVol.setGeometry(300, 200, 80, 40)
        self.diode_volLab.setGeometry(100, 300, 80, 40)
        self.diode_volLen.setGeometry(200, 300, 80, 40)
        self.diode_comboBoxVol.setGeometry(300, 300, 80, 40)
        self.cap_volLab.close()
        self.test_VoltageValue = 5
        self.cap_volLen.close()
        self.cap_comboBoxVol.close()
        self.diode_volLab.close()
        self.diode_volLen.close()
        self.diode_comboBoxVol.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Gui()

    sys.exit(app.exec_())
