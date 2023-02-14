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

from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QApplication,QMainWindow)
import sys


class testView(QWidget):

    def __init__(self):
        super().__init__()

        self.initUIView()

    def initUIView(self):

        self.lbl = QLabel("Ubuntu", self)

        self.combo = QComboBox(self)
        self.combo.addItem("Ubuntu")
        self.combo.addItem("Mandriva")
        self.combo.addItem("Fedora")
        self.combo.addItem("Arch")
        self.combo.addItem("Gentoo")

        self.combo.move(50, 50)
        self.lbl.move(50, 150)

        # self.combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    # def onActivated(self, text):

    #     self.lbl.setText(text)
    #     self.lbl.adjustSize()
    #     print(text)


# if __name__ == '__main__':

#     app = QApplication(sys.argv)
#     ex = testView()
#     sys.exit(app.exec_())