# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import sys
from yzm_image import ValidCodeImg
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QIcon


from chat_client import *




class child2_window(QDialog):
    code = ''
    def __init__(self, s):
        super().__init__()
        self.s = s
        self.resize(500, 330)
        self.setFixedWidth(500)
        # 调用窗口居中方法
        self.center()
        # 设置窗口标题
        self.setWindowTitle('注册')
        self.setWindowIcon(QIcon('./res/log.ico'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        self.label1 = QLabel(self)
        self.label1.setPixmap(QPixmap('timg1.jpg'))
        self.label1.setScaledContents(True)
        self.label1.setGeometry(0, 0, 500, 330)
        self.label2 = QLabel(self)
        self.label2.setStyleSheet(
            'QLabel{background-color:rgba(255,255,255,0.5);border-radius:5%}')
        self.label2.setScaledContents(True)
        self.label2.setGeometry(80, 50, 340, 230)

        self.lbl1 = QLabel(self, objectName='lbl')
        self.lbl1.setText('________________________________________')
        # self.lbl1.setScaledContents (True)
        self.lbl2 = QLabel(self, objectName='lbl1')
        self.lbl2.setText('________________________________________')
        # self.lbl2.setScaledContents (True)
        self.lbl3 = QLabel(self, objectName='lbl')
        self.lbl3.setText('________________________________________')
        # self.lbl3.setScaledContents (True)
        self.lbl4 = QLabel(self, objectName='lbl1')
        self.lbl4.setText('________________________________________')
        # self.lbl4.setScaledContents (True)
        self.lbl1.setGeometry(125, 70, 250, 50)
        self.lbl2.setGeometry(125, 120, 250, 50)
        self.lbl3.setGeometry(125, 165, 250, 50)
        self.lbl4.setGeometry(125, 210, 250, 50)
        # self.lbl5 = QLabel(self)
        # self.lbl5.setPixmap(QPixmap('test.png'))
        # self.lbl5.setScaledContents(True)
        # self.lbl5.setGeometry(245,210,120,30)

        self.textbox1 = QLineEdit(self)
        self.textbox3 = QLineEdit(self)
        self.textbox4 = QLineEdit(self)
        self.textbox2 = QLineEdit(self)

        self.textbox1.setFrame(False)
        self.textbox2.setFrame(False)
        self.textbox3.setFrame(False)
        self.textbox4.setFrame(False)

        self.textbox1.setPlaceholderText('请输入您的昵称')
        self.textbox2.setPlaceholderText('请输入验证码')
        self.textbox3.setPlaceholderText('请输入密码')
        self.textbox4.setPlaceholderText('请再次输入密码')
        self.textbox3.setEchoMode(QLineEdit.Password)
        self.textbox4.setEchoMode(QLineEdit.Password)

        self.textbox1.setGeometry(125, 75, 250, 25)
        self.textbox2.setGeometry(125, 215, 250, 25)
        self.textbox3.setGeometry(125, 125, 250, 25)
        self.textbox4.setGeometry(125, 170, 250, 25)

        self.btn = QPushButton(self)
        img = ValidCodeImg()
        child2_window.code = img.getValidCodeImg()
        self.btn.setStyleSheet('QPushButton{background-image:url("test.png");}')
        self.btn.setGeometry(245,210,120,30)
        self.btn.setToolTip('点击更换验证码')
        self.btn.clicked.connect(self.change_code)

        self.button = QPushButton('确认', self)
        self.button.setStyleSheet('QPushButton:hover{color:blue;}'
                                  'QPushButton{background-color:lightskyblue;color:white;}'
                                  'QPushButton{border-radius:10%}')
        self.button1 = QPushButton('取消', self)
        self.button1.setStyleSheet('QPushButton:hover{color:blue;}'
                                   'QPushButton{background-color:lightskyblue;color:white;}'
                                   'QPushButton{border-radius:10%}')
        self.button.setGeometry(125, 250, 50, 20)
        self.button1.setGeometry(325, 250, 50, 20)

        self.setStyleSheet('QLineEdit{background-color:rgba(255,255,255,0);font-size:14px;}'
                           "QLineEdit{color:black}"
                           "QLineEdit:hover{color:red}"
                           'QPushButton{border:none;background-color:rgba(255,255,255,0);}'
                           '#min:hover,#max:hover,#close:hover{background-color:red;}'
                           'QLabel{color:marom;}')

        self.minButton = QPushButton('0', self, objectName='min')
        self.minButton.setFont(QFont("Webdings"))
        self.minButton.clicked.connect(self.showMinimized)
        self.maxButton = QPushButton('1', self, objectName='max')
        self.maxButton.setFont(QFont("Webdings"))
        self.maxButton.clicked.connect(self.showmaximized)
        self.closeButton = QPushButton('r', self, objectName='close')
        self.closeButton.setFont(QFont("Webdings"))
        self.closeButton.clicked.connect(self.close)

        self.minButton.setGeometry(410, 0, 30, 30)
        self.maxButton.setGeometry(440, 0, 30, 30)
        self.closeButton.setGeometry(470, 0, 30, 30)

        self.button.clicked.connect(self.signalCall)

    def showmaximized(self):
        if self.maxButton.text() == '1':
            # 最大化
            self.maxButton.setText('２')
            self.showMaximized()
        else:  # 还原
            self.maxButton.setText('1')
            self.showNormal()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def change_code(self,image):
        # from yzm_image import ValidCodeImg
        img = ValidCodeImg()
        child2_window.code = img.getValidCodeImg()
        self.btn.setStyleSheet('QPushButton{background-image:url("test.png");}')
        print(child2_window.code)
    def signalCall(self):
        import random as R
        import account as a

        name = self.textbox1.text()
        input_code = self.textbox2.text()
        account = ''.join(str(i) for i in R.sample(range(1, 10), 8))
        passwd = self.textbox3.text()
        repasswd = self.textbox4.text()

        if passwd == repasswd and (account != "" and passwd != "" and repasswd != ""):
            if input_code.lower() == child2_window.code.lower():
                data = do_register(account, passwd, name, self.s)
                if data == name:
                    print(name + "注册成功")
                    from qq_main import main_window
                    self.a = main_window(self.s)
                    # self.cp = child1_window(self.s)  # 修改密码
                    # self.d = child2_window(self.s)  # 注册
                    # self.c = update_phone(self.s)
                    # self.f = do_forget(self.s)

                    # self.a.button.clicked.connect(self.a.signalCall)
                    # self.a.button1.clicked.connect(self.cp.show)
                    # self.a.button1.clicked.connect(self.a.close)
                    # self.a.button2.clicked.connect(self.d.show)
                    # self.a.button2.clicked.connect(self.a.close)
                    # self.a.btn.clicked.connect(self.c.show)
                    # self.a.btn.clicked.connect(self.a.close)
                    # self.a.btn1.clicked.connect(self.f.show)
                    # self.a.btn1.clicked.connect(self.a.close)

                    self.button1.clicked.connect(self.a.show)
                    self.button1.clicked.connect(self.close)

                    # self.cp.button1.clicked.connect(self.a.show)
                    # self.cp.button1.clicked.connect(self.cp.close)
                    #
                    # self.c.button1.clicked.connect(self.a.show)
                    # self.c.button1.clicked.connect(self.c.close)
                    #
                    # self.f.button1.clicked.connect(self.a.show)
                    # self.f.button1.clicked.connect(self.f.close)

                    # self.a.show()
                    # self.hide()
                    self.g = a.account(account, self.s)
                    self.g.show()
                    self.close()

                elif data == "Exists":
                    reply = QMessageBox.question(
                        self, '本程序', '用户已经存在', QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        print("用户已经存在")
                elif data == "RN":
                    reply = QMessageBox.question(
                        self, '本程序', '昵称已经存在', QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        print("昵称已经存在")
                else:
                    reply = QMessageBox.question(
                        self, '本程序', '注册失败', QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        print("用户已经存在")
            else:
                self.textbox2.clear()
                self.textbox3.clear()
                self.textbox4.clear()
                QMessageBox.question(self,'本程序','验证码错误',QMessageBox.Yes)
        else:
            self.textbox1.clear()
            self.textbox2.clear()
            self.textbox3.clear()
            self.textbox4.clear()
            reply = QMessageBox.question(
                self, '本程序', '两次密码不一致', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                # self.show()
                print("两次密码不一致")
