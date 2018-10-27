from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from qq_main import main_window
from zhuce import *
from update_phone import *
from do_forget import *



class child1_window(QDialog):
    signal = pyqtSignal(str)
    def __init__(self,s):
        super().__init__()
        self.s = s
        self.initUI()
    

    def initUI(self):
        self.resize(450, 330)
        self.setFixedWidth(450)
        # 调用窗口居中方法
        self.center()
        # 设置窗口标题
        self.setWindowTitle('修改密码')
        self.setWindowIcon(QIcon('./res/log.ico'))
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.label1 = QLabel(self)
        self.label1.setPixmap(QPixmap('./img/timg1.jpg'))
        self.label1.setScaledContents(True)
        self.label1.setGeometry(0, 0, 450, 130)
        self.label2 = QLabel(self)
        self.label2.setStyleSheet('QLabel{background-color:white;}')
        self.label2.setScaledContents(True)
        self.label2.setGeometry(0, 130, 450, 200)

        self.textbox = QLineEdit(self)
        self.textbox1 = QLineEdit(self)
        self.textbox2 = QLineEdit(self)

        self.textbox.setMaxLength(20)
        self.textbox1.setMaxLength(16)
        self.textbox2.setMaxLength(16)

        self.textbox.setPlaceholderText('账号')
        self.textbox1.setPlaceholderText('输入6-12原密码')
        self.textbox2.setPlaceholderText('输入6-12新密码')
        self.textbox.setStyleSheet('QLineEdit{background-color:rgba(255,255,255,0.5);font-size:18px;}'
                                   "QLineEdit{color:black}"
                                   "QLineEdit:hover{color:red}")
        self.textbox1.setStyleSheet('QLineEdit{background-color:rgba(255,255,255,0.5);font-size:18px;}'
                                    "QLineEdit{color:black}"
                                    "QLineEdit:hover{color:red}")
        self.textbox2.setStyleSheet('QLineEdit{background-color:rgba(255,255,255,0.5);font-size:18px;}'
                                    "QLineEdit{color:black}"
                                    "QLineEdit:hover{color:red}")

        self.textbox1.setEchoMode(QLineEdit.Password)
        self.textbox2.setEchoMode(QLineEdit.Password)

        # self.lbl.move(70,175)
        # self.lbl1.move(60,215)
        # self.lbl2.move(60,255)
        self.textbox.setGeometry(100, 170, 250, 30)
        self.textbox1.setGeometry(100, 210, 250, 30)
        self.textbox2.setGeometry(100, 250, 250, 30)

        self.button = QPushButton('确认', self)
        self.button.setGeometry(100, 295, 50, 25)
        self.button.setStyleSheet('QPushButton:hover{color:blue;}'
                                  'QPushButton{background-color:lightskyblue;color:white;}'
                                  'QPushButton{border-radius:10%}')

        self.button1 = QPushButton('返回', self)
        self.button1.setGeometry(300, 295, 50, 25)
        self.button1.setStyleSheet('QPushButton:hover{color:blue;}'
                                   'QPushButton{background-color:lightskyblue;color:white;}'
                                   'QPushButton{border-radius:10%}')

        self.minButton = QPushButton('0', self, objectName='min')
        self.minButton.setFont(QFont("Webdings"))
        self.minButton.clicked.connect(self.showMinimized)
        self.maxButton = QPushButton('1', self, objectName='max')
        self.maxButton.setFont(QFont("Webdings"))
        self.maxButton.clicked.connect(self.showmaximized)
        self.closeButton = QPushButton('r', self, objectName='close')
        self.closeButton.setFont(QFont("Webdings"))
        self.closeButton.clicked.connect(self.close)
        self.setStyleSheet('QPushButton{border:none;background-color:rgba(255,255,255,0);}'
                           'QPushButton:hover{background-color:red;}')

        self.minButton.setGeometry(360, 0, 30, 30)
        self.maxButton.setGeometry(390, 0, 30, 30)
        self.closeButton.setGeometry(420, 0, 30, 30)

        self.button.clicked.connect(self.signalCall)


    def showmaximized(self):
        if self.maxButton.text() == '1':
             # 最大化
             self.maxButton.setText('２')
             self.showMaximized()
        else:  # 还原
            self.maxButton.setText('1')
            self.showNormal()

    def signalCall(self):
        account = self.textbox.text()
        self.textbox.setText('')
        passwd = self.textbox1.text()
        self.textbox1.setText('')
        newpasswd = self.textbox2.text()
        self.textbox2.setText('')

        if passwd=='' or account == '' or newpasswd == '':
            reply = QMessageBox.question(self, '本程序', '消息不能为空', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print("消息不能为空")
        else:
            msg = change_passwd(account,passwd,newpasswd,self.s)
            if msg == "OK":
                reply = QMessageBox.question(self, '本程序', '修改密码成功', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.a = main_window(self.s)
                    self.cp = child1_window(self.s)#修改密码
                    self.d = child2_window(self.s)#注册
                    self.c = update_phone(self.s)
                    self.f = do_forget(self.s)
                    self.a.button.clicked.connect(self.a.signalCall)
                    self.a.button1.clicked.connect(self.cp.show)
                    self.a.button1.clicked.connect(self.a.close)
                    self.a.button2.clicked.connect(self.d.show)
                    self.a.button2.clicked.connect(self.a.close)
                    self.a.btn.clicked.connect(self.c.show)
                    self.a.btn.clicked.connect(self.a.close)
                    self.a.btn1.clicked.connect(self.f.show)
                    self.a.btn1.clicked.connect(self.a.close)

                    self.d.button1.clicked.connect(self.a.show)
                    self.d.button1.clicked.connect(self.d.hide)

                    self.cp.button1.clicked.connect(self.a.show)
                    self.cp.button1.clicked.connect(self.cp.close)

                    self.c.button1.clicked.connect(self.a.show)
                    self.c.button1.clicked.connect(self.c.close)

                    self.f.button1.clicked.connect(self.a.show)
                    self.f.button1.clicked.connect(self.f.close)

                    self.a.show()
                    self.hide()
                    print("修改密码成功")
            elif msg == "FALL":
                reply = QMessageBox.question(self, '本程序', '修改密码失败', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print("修改密码失败")
            elif msg == "NP":
                reply = QMessageBox.question(self, '本程序', '密码不正确', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print("修改密码失败")
            elif msg == "NI":
                reply = QMessageBox.question(self, '本程序', '没有该用户', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print("修改密码失败")


    def center(self): 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())