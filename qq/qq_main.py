# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from chat_client import *
from qq import *
from socket import *
from xiugaimima import *
from do_forget import *
from main import *

from update_phone import *
import sys


class main_window(QWidget):

    def __init__(self, s):
        super().__init__()
        self.s = s
        # self.setObjectName("MainWindow")
        # self.setStyleSheet("#MainWindow{border-image:url('timg.jpg');}")
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口标题
        self.setWindowTitle('登陆')
        self.setWindowIcon(QIcon('./res/log.ico'))
        # 设置窗口大小
        self.resize(450, 330)
        self.setFixedWidth(450)

        # 调用窗口居中方法
        self.center()
        self.initUI()

    def initUI(self):
        self.label1 = QLabel(self)
        self.movie = QMovie("timg.gif")
        self.label1.setMovie(self.movie)
        self.movie.start()
        # self.label1.setPixmap(QPixmap("image/qq_background.jpg"))
        self.label1.setScaledContents(True)
        self.label1.setGeometry(0, 0, 450, 130)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("image/imlogo_b.png"))
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, 60, 35)
        self.label2 = QLabel(self)
        self.label2.setStyleSheet('QLabel{background-color:aliceblue;}')
        self.label2.setScaledContents(True)
        self.label2.setGeometry(0, 130, 450, 200)
        self.btn = QPushButton(self)
        # self.label3 = QLabel(self)
        self.btn.setStyleSheet(
            'QPushButton{border-radius:35%;background-image:url("img/image.jpg");}')
        # 'QPushButton{border-radius:35%;}')
        # self.btn.setPixmap(QPixmap("image/qq_background.jpg"))
        # self.btn.setScaledContents (True)
        self.btn.setGeometry(180, 90, 70, 70)

        self.usericon = QLabel(self)
        self.usericon.setGeometry(70, 175, 24, 24)
        self.usericon.setPixmap(QPixmap("img/account.png"))
        self.pwdicon = QLabel(self)
        self.pwdicon.setGeometry(70, 215, 24, 24)
        self.pwdicon.setPixmap(QPixmap("img/password.png"))

        self.lbl = QLabel(self, objectName='lbl')
        self.lbl.setText('________________________________________')
        # self.lbl.setScaledContents (True)
        self.lbl1 = QLabel(self, objectName='lbl1')
        self.lbl1.setText('________________________________________')
        # self.lbl1.setScaledContents (True)
        self.lbl.setGeometry(100, 170, 250, 50)
        self.lbl1.setGeometry(100, 210, 250, 50)

        self.textbox = QLineEdit(self, objectName='textbox')
        self.textbox.setMaxLength(20)
        self.textbox.setPlaceholderText(' 账号')
        self.textbox1 = QLineEdit(self, objectName='textbox1')
        self.textbox1.setMaxLength(16)
        self.textbox1.setPlaceholderText('密码')
        self.textbox1.setEchoMode(QLineEdit.Password)
        self.textbox.setGeometry(100, 170, 250, 30)
        self.textbox1.setGeometry(100, 210, 250, 30)
        self.textbox.setFrame(False)
        self.textbox1.setFrame(False)
        self.textbox.setStyleSheet('QLineEdit{background-color:rgba(255,255,255,0);font-size:18px;}'
                                   "QLineEdit{color:black}"
                                   "QLineEdit:hover{color:red}")
        self.textbox1.setStyleSheet("QLineEdit{color:black}"
                                    "QLineEdit:hover{color:red}"
                                    "QLineEdit{background-color:rgba(255, 255, 255, 0);font-size:18px;}"
                                    "QLineEdit{padding:2px 4px}")

        # 建立控件对象
        self.btn = QPushButton('绑定/修改手机号', self)
        self.btn.setStyleSheet('QPushButton:hover{color:red;}')
        self.btn1 = QPushButton('忘记密码', self)
        self.btn1.setStyleSheet('QPushButton:hover{color:red;}')
        self.button = QPushButton('登陆', self)
        self.button.setStyleSheet(
            'QPushButton{background-color:lightskyblue;color:white;border-radius:5%;font-size:18px;}''QPushButton:hover{color:blue}')
        self.button1 = QPushButton('修改密码', self)
        self.button1.setStyleSheet('QPushButton:hover{color:red;}')
        self.button2 = QPushButton('注册账号', self)
        self.button2.setStyleSheet('QPushButton:hover{color:red;}')
        # 设置控件提示语
        self.button.setToolTip('点击登陆')
        self.button2.setToolTip('没有账号?点击注册')
        # 设置控件位置及大小
        self.btn.setGeometry(100, 245, 100, 25)
        self.btn1.setGeometry(300, 245, 50, 25)
        self.button.setGeometry(100, 275, 250, 35)
        self.button1.setGeometry(385, 295, 50, 25)
        self.button2.setGeometry(15, 295, 50, 25)

        self.minButton = QPushButton('0', self, objectName='min')
        self.minButton.setFont(QFont("Webdings"))
        self.minButton.clicked.connect(self.showMinimized)

        self.maxButton = QPushButton('1', self, objectName='max')
        self.maxButton.setFont(QFont("Webdings"))
        self.maxButton.clicked.connect(self.showmaximized)

        self.closeButton = QPushButton('r', self, objectName='close')
        self.closeButton.setFont(QFont("Webdings"))
        self.closeButton.clicked.connect(self.close)

        self.setStyleSheet(
            'QPushButton{border:none;}#min:hover,#max:hover,#close:hover{background-color:red;}')

        self.minButton.setGeometry(360, 0, 30, 30)
        self.maxButton.setGeometry(390, 0, 30, 30)
        self.closeButton.setGeometry(420, 0, 30, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def showmaximized(self):
        if self.maxButton.text() == '1':
            # 最大化
            self.maxButton.setText('２')
            self.showMaximized()
        else:  # 还原
            self.maxButton.setText('1')
            self.showNormal()

    def center(self):
         # 将窗口居中放置的代码在自定义的center()方法中
        qr = self.frameGeometry()
        # 获得主窗口的一个矩形特定几何图形，这包含了窗口的框架
        cp = QDesktopWidget().availableGeometry().center()
        # 算出相对于显示器的绝对值。并且从这个绝对值中，我们获得了屏幕中心点
        qr.moveCenter(cp)
        # 把矩形的中心设置到屏幕的中间去
        self.move(qr.topLeft())

    def signalCall(self):
        account = self.textbox.text()
        self.textbox.setText('')
        passwd = self.textbox1.text()
        self.textbox1.setText('')
        account, name = do_login(account, passwd, self.s)
        if name != 1:
            self.b = QQ(self.s, account)
            self.b.show()
            self.close()
        else:
            reply = QMessageBox.question(self, '本程序', '登录失败', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print('登录失败')

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 5111
    ADDR = (HOST, PORT)
    sockfd = socket()
    sockfd.connect(ADDR)

    app = QApplication(sys.argv)
    a = main_window(sockfd)  # 登录界面
    a.show()
    c = child1_window(sockfd)  # 修改密码界面
    d = child2_window(sockfd)  # 注册界面
    f = do_forget(sockfd)  # 忘记密码界面
    e = update_phone(sockfd)
    # cp = MainWindow()#聊天界面
    # 点击按钮跳转窗口
    a.button.clicked.connect(a.signalCall)
    a.button1.clicked.connect(c.show)
    a.button1.clicked.connect(a.close)
    a.button2.clicked.connect(d.show)
    a.button2.clicked.connect(a.close)
    a.btn.clicked.connect(e.show)
    a.btn.clicked.connect(a.close)
    a.btn1.clicked.connect(f.show)
    a.btn1.clicked.connect(a.close)
    c.button1.clicked.connect(a.show)
    c.button1.clicked.connect(c.hide)
    d.button1.clicked.connect(a.show)
    d.button1.clicked.connect(d.hide)
    f.button1.clicked.connect(a.show)
    f.button1.clicked.connect(f.hide)
    e.button1.clicked.connect(a.show)
    e.button1.clicked.connect(e.hide)
    sys.exit(app.exec_())
