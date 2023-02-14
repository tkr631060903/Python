# coding: utf-8
from corelib.autolib import ATS
import os
import sys
# from io import BytesIO
# from threading import Thread
from corelib.immsg import IMMsg
from devLibs.devInfo.devInfo import devInfo
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLabel, QFileDialog, QScrollArea, QSizePolicy, QInputDialog, QPushButton
from PySide2.QtCore import QFile, QObject, Slot, QTimer, QSize, Qt
from PySide2.QtGui import QIcon, QKeySequence, QClipboard
from PySide2.QtGui import QImage, QPalette, QPixmap
import shutil

import win32gui
import win32api
import win32con
from time import sleep

class Dialog():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self, title):
        self.hwnd = win32gui.FindWindow('#32770', title)

    def ClickButtonByTitel(self, title):
        assert self.hwnd
        hbtn = win32gui.FindWindowEx(self.hwnd,0,'Button',title)
        assert hbtn
        win32api.PostMessage(hbtn, win32con.WM_LBUTTONDOWN, 0, 0)
        win32api.PostMessage(hbtn, win32con.WM_LBUTTONUP, 0, 0)

    def CheckButtonByTitel(self, title, check = 1):
        assert self.hwnd
        hbtn = win32gui.FindWindowEx(self.hwnd,0,'Button',title)
        assert hbtn      
        win32api.PostMessage(hbtn, win32con.BM_SETCHECK, check, 0)

        # hbtn.SendMessage(win32con.BM_SETSTATE,  1, 0 )
    def InputEditByIndex(self, index, text):
        assert self.hwnd
        heditfirst= win32gui.FindWindowEx(self.hwnd,0,'Edit',None)
        hedit = heditfirst
        for i in range(index):
            hedit = win32gui.FindWindowEx(self.hwnd,hedit,'Edit',None)
        assert hedit
        win32gui.SendMessage(hedit, win32con.WM_SETTEXT, None, text)


class UI(QObject):
    def __init__(self, ui, path):
        super().__init__()
        self.thispath = path
        self.dev = devInfo()
        self.savepath = self.dev.getAddr("Screenshot")
        if self.savepath == "":
            self.savepath = "D:/Image"

        self.menu = {
            "设置": {
                "置顶窗口#": "setOnTop()",
                "图片标题@QKeySequence.New": "getImageTitle()",
                "存储路径@'Ctrl+O'": "getPath()",
                "消息通知@'Ctrl+M'": "getUser()",
            },
            "查看": {
                "后退@QKeySequence.MoveToPreviousChar": "getPre()",
                "前进@QKeySequence.MoveToNextChar": "getNext()",
            },
            "截图@QKeySequence.Save": "getScreenshot()",
            # "帮助@QKeySequence.HelpContents": "help()"
        }
        self.use_devices = ['示波器']

        # 标准快捷键,参考下面网址
        # https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html#standard-shortcuts

        self.ui = ui
        self.menubar = ui.menubar
        self.statusbar = ui.statusbar

        self.checked = True
        self.user = ""
        # self.dis = ui.listSet
        # 所有信号槽操作,必须先添加menu
        self.creatMenus(self.menubar, self.menu)
        # 创建状态栏
        self.createStatusbar()
        # 创建图片显示
        # self.createImageLable()
        # 设置窗口置顶
        self.setOnTop()
        self.ui.btnBOM.clicked.connect(outBOM)
        ui.show()
        # 连接示波器
        # self.connectScope()
        # self.cap = Cap()

    def createImageLable(self):
        self.clipboard = QClipboard()
        self.image = ""
        self.image_title = ""
        self.image_list = []
        self.image_index = 0
        self.imageLabel = QLabel("示波器截图")
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        # ui.mainLayout.addWidget(self.scrollArea)
        ui.setCentralWidget(self.scrollArea)
        self.defimage = QImage(self.thispath + "/ui/images/logo.png")
        self.displayImage(self.defimage, 1.0)

    def createStatusbar(self):
        self.statusLabel = QLabel(" ")
        self.pathLabel = QLabel(" 路径[Ctrl+O] " + self.savepath + " ")
        self.titleLabel = QLabel(" 标题[Ctrl+N] ")
        self.imLabel = QLabel(" 截图[Ctrl+S] ")

        self.statusbar.addWidget(self.statusLabel)
        self.statusbar.addWidget(self.pathLabel)
        self.statusbar.addWidget(self.titleLabel)
        # 控件扩展至最大
        self.statusbar.addWidget(self.imLabel, 1)
        self.statusbar.setSizeGripEnabled(True)
    
    def help(self):
        print("help")

    def getPath(self):
        path = QFileDialog.getExistingDirectory(
            self.ui, "选择存储路径", self.savepath, QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks)
        if path != "":
            self.savepath = path
            self.pathLabel.setText(" 路径[Ctrl+O] " + self.savepath + " ")
            self.dev.setAddr("Screenshot", self.savepath)

    def getUser(self):
        user, ok = QInputDialog.getText(
            self.ui,
            "请输入",
            "用户名:",
            flags=Qt.WindowCloseButtonHint,
            text=self.user)
        if ok:
            self.user = user
            self.cap.setUsr(self.user)
        # if ok and text:
        #     textLabel.setText(text)
    
    def setOnTop(self):
        print(self.checked)
        if self.checked:
            self.ui.setWindowFlags(self.ui.windowFlags()
                                   | Qt.WindowStaysOnTopHint)
        else:
            self.ui.setWindowFlags(self.ui.windowFlags()
                                   & (~Qt.WindowStaysOnTopHint))
        self.ui.show()

    @Slot()
    def menu_triggered(self, check):
        self.checked = check
        action = self.sender().text()
        self.runMenuFunc(action, self.menu)
    def outBOM(self):
        dialog = Dialog('Bill of Materials')
        if dialog.hwnd != 0:
            dialog.ClickButtonByTitel('Process &entire design')
            dialog.ClickButtonByTitel('Use instances (Preferred)')
            dialog.CheckButtonByTitel('Open in E&xcel',1)   
            dialog.CheckButtonByTitel('Place each part entry on a separate &line',0) 
            dialog.InputEditByIndex(0,'Item\\tQuantity\\tValue\\tValue Brief\\tReference\\tAEC Qualified\\tpcb footprint')
            dialog.InputEditByIndex(1,'{Item}\\t{Quantity}\\t{Value}\\t{Value Brief}\\t{Reference}\\t{AEC Qualified}\\t{pcb footprint}')
            dialog.ClickButtonByTitel('OK')
            # print('执行BOM导出完毕')
            self.statusLabel.setText(" 执行BOM导出完毕 ")
    def runMenuFunc(self, action, menu):
        for item in menu:
            if type(menu[item]) is str:
                if action in item:
                    eval("self." + menu[item])
                    break
            else:
                self.runMenuFunc(action, menu[item])

    def creatMenus(self, menubar, menu):
        for item in menu:
            if type(menu[item]) is str:
                action = menubar.addAction(item.split("@")[0].split("#")[0])
                action.triggered.connect(self.menu_triggered)
                if "@" in item:
                    action.setShortcut(QKeySequence(eval(item.split("@")[1])))
                if "#" in item:
                    action.setCheckable(True)
                    action.setChecked(True)
            else:
                self.creatMenus(menubar.addMenu(item), menu[item])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    thisfiledir = os.path.dirname(__file__)

    ui_file = QFile(thisfiledir + "/ui/capture.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    ui = loader.load(ui_file)
    # 更改LOGO
    ui.setWindowIcon(QIcon(thisfiledir + '/ui/images/logo.png'))
    ate = UI(ui, thisfiledir)
    sys.exit(app.exec_())
