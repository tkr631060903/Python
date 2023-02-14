#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
ZetCode PyQt5 tutorial 

This example shows how to use 
a QComboBox widget.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
import os

sys.path.append(os.path.realpath("."))

from PyQt5.QtWidgets import (QWidget, QApplication,QMainWindow)

from Gui.UIView_test.testView import testView



class testFunction(testView, QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.initUIView()
        self.initUI()
        # self.data=0

    def initUI(self):
        self.combo.activated[str].connect(self.onActivated)
        self.data=0

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
        print(text)

class testData(testFunction,QWidget):
    def __init__(self):
        super(testData,self).__init__()
        print(self.data)
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = testFunction()
    # da = testData()
    sys.exit(app.exec_())