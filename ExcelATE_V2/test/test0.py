import sys
import qdarkstyle
from PyQt5.QtCore import Qt, QTimer, QDateTime, QDate, QFile
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QTextEdit, QGroupBox,
    QCheckBox, QRadioButton, QComboBox, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QStyleFactory, QTabWidget, QSizePolicy, QProgressBar,
    QTableWidget, QLineEdit, QSpinBox, QDateTimeEdit, QSlider, QScrollBar,
    QMenu, QMenuBar, QAction, QCalendarWidget, QDial)


#标记控制窗口
class DarkStyleSheetDemo(QMainWindow):

    def __init__(self):
        super(DarkStyleSheetDemo, self).__init__()

        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: QDarkStyleSheet 演示')

        #应用的初始调色板
        self.origPalette = QApplication.palette()

        self.initUi()

    def initUi(self):
        self.initMenuBar()

        #生成要显示的部件
        self.createTopLeftGroupBox()
        self.createTopLeftGroupBox1()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)  #1行0列
        mainLayout.addWidget(self.topLeftGroupBox1, 1, 0)  #1行0列
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)  #1行1列
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)  #2行0列
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)  #2行1列
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)  ## 3行0列，占1行2列
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)

    #菜单栏设置
    def initMenuBar(self):
        mBar = self.menuBar()

        menuFile = mBar.addMenu('文件(&F)')
        aExit = QAction('退出(&X)', self)
        aExit.triggered.connect(self.close)
        menuFile.addAction(aExit)

    #创建左上角成组部件
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox('组 1')

        rad1 = QRadioButton('单选按钮1')
        rad2 = QRadioButton('单选按钮2')
        rad3 = QRadioButton('单选按钮3')
        # rad1.setChecked(True)

        chk = QCheckBox('三态复选按钮')
        # chk.setTristate(True)
        # chk.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(rad1)
        layout.addWidget(rad2)
        layout.addWidget(rad3)
        # layout.addWidget(chk)
        # layout.addStretch(1)

        self.topLeftGroupBox.setLayout(layout)

    #创建左上角成组部件1
    def createTopLeftGroupBox1(self):
        self.topLeftGroupBox1 = QGroupBox('组 1')

        rad1 = QRadioButton('单选按钮1')
        rad2 = QRadioButton('单选按钮2')
        rad3 = QRadioButton('单选按钮3')
        rad1.setChecked(True)

        chk = QCheckBox('三态复选按钮')
        chk.setTristate(True)
        chk.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(rad1)
        layout.addWidget(rad2)
        # layout.addWidget(rad3)
        # layout.addWidget(chk)
        # layout.addStretch(1)

        self.topLeftGroupBox1.setLayout(layout)

    def addbtn(self):
        self.layout1.addWidget(self.btnToggle, 0, 1)
        # self.layout1.itemAt(1).widget().show()
        self.btnToggle.show()
        self.topLeftGroupBox.show()
        self.topLeftGroupBox1.close()
        

    def btn(self):
        # self.layout1.addWidget(self.btnToggle, 0, 1)
        # self.layout1.removeWidget(self.btnToggle)
        self.topLeftGroupBox.close()
        self.topLeftGroupBox1.show()
        self.btnToggle.close()

    #创建右上角成组部件
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox('组 2')

        btnDefault = QPushButton('Push Button：缺省模式')
        btnDefault.clicked.connect(self.addbtn)
        btnDefault.setDefault(True)
        # btnDefault.setFixedSize(50,50)

        self.btnToggle = QPushButton('Push Button: 切换模式')
        self.btnToggle.setCheckable(True)
        self.btnToggle.setChecked(True)

        btnFlat = QPushButton('Push Button: 扁平外观')
        btnFlat.clicked.connect(self.btn)
        btnFlat.setFlat(True)

        self.layout1 = QGridLayout()
        self.layout1.addWidget(btnDefault,0,0)
        self.layout1.addWidget(self.btnToggle,0,1)
        self.layout1.addWidget(btnFlat,3,0)
        # self.layout1.addStretch(1)
        print(self.layout1.count())
        # self.layout1.itemAt(1).widget().hide()
        self.layout1.removeWidget(self.btnToggle)



        self.topRightGroupBox.setLayout(self.layout1)


    #创建左下角Tab控件
    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)  #10行10列

        tab1Layout = QHBoxLayout()
        tab1Layout.setContentsMargins(5, 5, 5, 5)
        tab1Layout.addWidget(tableWidget)
        tab1.setLayout(tab1Layout)

        tab2 = QWidget()
        textEdit = QTextEdit()
        textEdit.setPlainText("一闪一闪小星星,\n"
                              "我想知道你是什么.\n"
                              "在整个世界之上, 如此的高,\n"
                              "像在天空中的钻石.\n"
                              "一闪一闪小星星,\n"
                              "我多想知道你是什么!\n")

        tab2Layout = QHBoxLayout()
        tab2Layout.setContentsMargins(5, 5, 5, 5)
        tab2Layout.addWidget(textEdit)
        tab2.setLayout(tab2Layout)

        tab3 = QWidget()
        calendar = QCalendarWidget()
        #设置最小日期
        calendar.setMinimumDate(QDate(1900, 1, 1))
        #设置最大日期
        calendar.setMaximumDate(QDate(4046, 1, 1))
        #设置网格可见
        calendar.setGridVisible(True)
        tab3Layout = QHBoxLayout()
        tab3Layout.setContentsMargins(5, 5, 5, 5)
        tab3Layout.addWidget(calendar)
        tab3.setLayout(tab3Layout)

        self.bottomLeftTabWidget.addTab(tab1, '表格(&T)')
        self.bottomLeftTabWidget.addTab(tab2, '文本编辑(&E)')
        self.bottomLeftTabWidget.addTab(tab3, '日历(&C)')

        #self.bottomLeftTabWidget.addTab(tab1, '表格(&T)')
        #self.bottomLeftTabWidget.addTab(tab2, '文本编辑(&E)')

    #创建右下角成组部件
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox('组 3')
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)  #0行0列，占1行2列
        layout.addWidget(spinBox, 1, 0, 1, 2)  #1行0列，占1行2列
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)  #2行0列，占1行2列
        layout.addWidget(slider, 3, 0)  #3行0列，占1行1列
        layout.addWidget(scrollBar, 4, 0)  #4行0列，占1行1列
        layout.addWidget(dial, 3, 1, 2, 1)  #3行1列，占2行1列
        layout.setRowStretch(5, 1)

        self.bottomRightGroupBox.setLayout(layout)

    #禁止窗口上的组件
    def setWidgetsDisbaled(self, disable):
        self.topLeftGroupBox.setDisabled(disable)
        self.topRightGroupBox.setDisabled(disable)
        self.bottomLeftTabWidget.setDisabled(disable)
        self.bottomRightGroupBox.setDisabled(disable)

    #创建进度条
    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        # 定时器，定时更新进度条的值
        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(100)

    #设置进度条的值
    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DarkStyleSheetDemo()

    #设置样式表
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window.show()
    sys.exit(app.exec())
