#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.realpath("."))

from PyQt5 import QtWidgets
from Gui.UIFunction.UIFunction import UIFunctionClass

from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    extra = {

        # Button colors
        'danger': '#dc3545',
        'warning': '#ffc107',
        'success': '#17a2b8',

        # Font
        'font_family': 'SimSun',  # 修改字体
        'font_size': '20px',  # 字体大小
    }

    apply_stylesheet(app, theme = 'dark_teal.xml', extra = extra)  # 美化主题

    # font = QFont()
    # font.setPixelSize(100)
    # font.setFamily("SimHei")
    # app.setFont(font)

    ui = UIFunctionClass()

    sys.exit(app.exec_())

