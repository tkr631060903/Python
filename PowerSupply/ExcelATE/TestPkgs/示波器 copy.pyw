# coding: utf-8
import os
import sys
import json
import shutil
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLabel, QFileDialog, QScrollArea, QSizePolicy, QInputDialog
from PySide2.QtCore import QFile, QObject, Slot, QTimer, QSize, Qt
from PySide2.QtGui import QIcon, QKeySequence, QClipboard
from PySide2.QtGui import QImage, QPalette, QPixmap
from corelib.autolib import ATS
from corelib.immsg import IMMsg
from devLibs.devInfo.devInfo import devInfo
# from io import BytesIO
# from threading import Thread


class Cap():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.state = None
        self.start = False
        self.cfg = []

    def set_usr(self, usr):
        self.cfg.append({
            "id": 0,
            "usr": usr,
            "max": -1,
            "cnt": 0,
            "action": "完成|异常|终止",
            "max_img": -1,
            "cnt_img": 0
        })

    def get_state(self):
        try:
            self.state = ATS.myScope.get_state()
            if int(self.state) != 0:
                self.start = True
            else:
                if self.start:
                    self.start = False
                    return True
            return False
        except Exception as err:
            raise RuntimeError(err)

    def get_scope(self, filename, path):
        imagename = None
        try:
            if filename is not None:
                if filename != "":
                    filename = "-" + filename
                imagename = path + "/" + ATS.getScopeScreen(path, filename)
                # self.U_ClipboardImage(imagename)
                try:
                    msg = IMMsg(self.cfg)
                    msg.send({"action": "完成", "msg": imagename})
                except Exception:
                    pass
                return imagename
        except Exception as err:
            print("[process] get scope screen error:" + str(err))


class UI(QObject):
    def __init__(self, _ui, path):
        super().__init__()
        self.image_model = None
        self.thispath = path
        self.image = ""
        self.image_title = ""
        self.image_list = []
        self.image_index = 0
        self.imageLabel = QLabel("示波器截图")
        self.dev = devInfo()
        self.savepath = self.dev.getAddr("Screenshot")
        if self.savepath == "":
            self.savepath = "D:/Image"

        self.menu = {
            "设置": {
                "置顶窗口#": "setOnTop()",
                "存储路径@'Ctrl+P'": "getPath()",
                "消息通知@'Ctrl+M'": "getUser()",
            },
            "模板": {
                "新建模板@QKeySequence.New": "getImageModel()",
                "选择模板": {
                    "通用模板#": "selImageModel()",
                },
            },
            "查看": {
                "后退@QKeySequence.MoveToPreviousChar": "getPre()",
                "前进@QKeySequence.MoveToNextChar": "getNext()",
            },
            "截图@QKeySequence.Save": "getScreenshot()",
            # "帮助@QKeySequence.HelpContents": "help()"
        }
        cfg = None
        try:
            # 打开配置文件
            with open(path + '/ui/setting/Model.json', 'r',
                      encoding='UTF-8') as f:
                # 加载配置
                cfg = json.loads(f.read())
        except Exception:
            pass
        for item in cfg:
            self.menu["模板"]["选择模板"][item] = "selImageModel()"
        self.use_devices = ['示波器']

        # 标准快捷键,参考下面网址
        # https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html#standard-shortcuts

        self.ui = _ui
        self.menubar = ui.menubar
        self.statusbar = ui.statusbar

        self.checked = True
        self.user = ""
        # self.dis = ui.listSet
        # 所有信号槽操作,必须先添加menu
        self.creatMenus(self.menubar, self.menu)
        # 创建状态栏
        self.create_statusbar()
        # 创建图片显示
        self.create_imageLable()
        # 创建图片显示
        self.create_imageInfo()
        # 设置窗口置顶
        self.setOnTop()
        ui.show()
        # 连接示波器
        self.connect_scope()
        self.cap = Cap()

    def create_imageLable(self):
        self.clipboard = QClipboard()

        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.ui.imageLayout.addWidget(self.scrollArea)
        # ui.setCentralWidget(self.scrollArea)
        self.defimage = QImage(self.thispath + "/ui/images/logo.png")
        self.displayImage(self.defimage, 1.0)

    def create_imageInfo(self):
        pass
        # self.ui.tableInfo.hide()
        # self.ui.tableImageList.hide()
        # self.comboModel = QComboBox()
        # self.ui.mainLayout.addWidget(self.scrollArea)
        # # ui.setCentralWidget(self.scrollArea)
        # self.defimage = QImage(self.thispath + "/ui/images/logo.png")
        # self.displayImage(self.defimage, 1.0)

    def create_statusbar(self):
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

    def connect_scope(self):
        #
        QTimer.singleShot(1000, self.tryConnect)

    # 尝试连接
    def tryConnect(self):
        try:
            self.statusLabel.setText(" 正在尝试连接示波器.... ")
            # 更新资源列表
            ATS.dev_update()
            # 连接示波器
            ATS.connect_devices(self.use_devices)
            # 设备已连接
            self.statusLabel.setText(" 已连接 ")
            # 启动一次示波器状态监控
            QTimer.singleShot(1000, self.getMonitor)
            # 更新窗口标题
            title = ATS.myScope.IDN()
            self.ui.setWindowTitle("示波器截图 [" + title[0].split(" ")[0].upper() +
                                   " " + title[1].upper() + "]")
        except Exception as err:
            # 设备连接异常
            self.statusLabel.setText(str(err) + " !请检查示波器连接是否正常 ")
            # 定时再次尝试连接
            QTimer.singleShot(1000, self.tryConnect)

    def displayImage(self, image, scale):
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.imageLabel.resize(scale * self.imageLabel.pixmap().size())

    def getPre(self):
        if self.image_index > 0:
            # 获取图片名称
            image = self.image_list[self.image_index - 1]
            # 加载图片
            image, scale = self.loadFileImage(image, False)
            # 显示图片
            self.displayImage(image, scale)
        else:
            self.imLabel.setText(self.imLabel.text().split(" 当前是最")[0] +
                                 " 当前是最早的图片!")

    def getNext(self):
        if self.image_index + 1 < len(self.image_list):
            # 获取图片名称
            image = self.image_list[self.image_index + 1]
            # 加载图片
            image, scale = self.loadFileImage(image, False)
            # 显示图片
            self.displayImage(image, scale)
        else:
            self.imLabel.setText(self.imLabel.text().split(" 当前是最")[0] +
                                 " 当前是最新的图片!")

    def selImageModel(self, model):
        print(model)

    def loadFileImage(self, imagename, new=True):
        # 加载文件
        image = QImage(imagename)
        # 文件格式错误,重新加载
        if image.height() == 0:
            image = QImage(imagename, "bmp")
        if image.height() == 0:
            shutil.copy(imagename, imagename.split(".")[0])
            image = QImage(imagename.split(".")[0])
            os.remove(imagename.split(".")[0])
        scale = 1.0
        print(image.size())
        # 图片放大倍数
        if image.height() < 200:
            scale = 3.0
        elif image.height() < 300:
            scale = 2.0
        elif image.height() < 400:
            scale = 1.5
        # 窗口没有最大化
        if not self.ui.isMaximized():
            # 调整窗口大小适应图片显示
            self.ui.resize(
                QSize(image.width() * scale + 2,
                      image.height() * scale + 47))
        if new:
            # 是新获取的示波器截图,加入图片列表
            self.image_list.append(imagename)
        if image is None:
            self.statusLabel.setText(" 加载图片失败 ")
        else:
            # 获取图片索引
            self.image_index = self.image_list.index(imagename)
            # 更新状态栏
            self.imLabel.setText(" 截图[Ctrl+S] " + imagename.split("/")[-1])
            # 设置粘贴板
            self.clipboard.setImage(image)
        return image, scale

    def loadScopeImage(self):
        # 获取一次示波器截图
        image = self.cap.get_scope(self.image_title, self.savepath)
        # 加载图片
        image, scale = self.loadFileImage(image, True)
        # 显示图片
        self.displayImage(image, scale)
        # 截图任务执行完成,启动一次示波器状态监控
        QTimer.singleShot(1000, self.getMonitor)

    def getScreenshot(self):
        # 显示默认背景图
        self.displayImage(self.defimage, 1.0)
        # 启动一次获取示波器截图
        QTimer.singleShot(100, self.loadScopeImage)

    def getMonitor(self):
        try:
            if self.cap.get_state():
                # 需要截图
                # 显示默认背景图
                self.displayImage(self.defimage, 1.0)
                # 启动一次获取示波器截图
                QTimer.singleShot(100, self.loadScopeImage)
            else:
                # 无需执行截图任务,启动一次示波器状态监控
                QTimer.singleShot(1000, self.getMonitor)
        except Exception:
            self.connectScope()

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
        user, ok = QInputDialog.getText(self.ui,
                                        "请输入",
                                        "用户名:",
                                        flags=Qt.WindowCloseButtonHint,
                                        text=self.user)
        if ok:
            self.user = user
            self.cap.set_usr(self.user)
        # if ok and text:
        #     textLabel.setText(text)

    def getImageModel(self):
        title, ok = QInputDialog.getText(self.ui,
                                         "请输入",
                                         "模板名称:",
                                         flags=Qt.WindowCloseButtonHint,
                                         text=self.image_model)
        if ok:
            self.image_model = title
        self.titleLabel.setText(" 新建模板[Ctrl+N] " + self.image_model)

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
    App = QApplication(sys.argv)
    this_filedir = os.path.dirname(__file__)

    ui_file = QFile(this_filedir + "/ui/scope.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    ui = loader.load(ui_file)
    # 更改LOGO
    ui.setWindowIcon(QIcon(this_filedir + '/ui/images/logo.png'))
    ate = UI(ui, this_filedir)
    sys.exit(App.exec_())
