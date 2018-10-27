# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from xiugaimima import *
from zhuce import child2_window
from yuyin import *
from chat_client import *
import random as R
import sys
import re

from update_phone import *


class do_forget(QDialog):
    code = ''

    def __init__(self, s):
        super().__init__()
        self.s = s
        self.resize(500, 330)
        self.setFixedWidth(500)
        # 调用窗口居中方法
        self.center()
        # 设置窗口标题
        self.setWindowTitle('忘记密码')
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

        self.textbox1 = QLineEdit(self)
        self.textbox2 = QLineEdit(self)
        self.textbox3 = QLineEdit(self)
        self.textbox4 = QLineEdit(self)

        self.textbox1.setFrame(False)
        self.textbox2.setFrame(False)
        self.textbox3.setFrame(False)
        self.textbox4.setFrame(False)

        self.textbox1.setPlaceholderText('请输入账号')
        self.textbox2.setPlaceholderText('请输入手机号')
        self.textbox3.setPlaceholderText('请输入验证码')
        self.textbox4.setPlaceholderText('请输入新密码')
        # self.textbox3.setEchoMode(QLineEdit.Password)
        self.textbox4.setEchoMode(QLineEdit.Password)

        self.textbox1.setGeometry(125, 75, 250, 25)
        self.textbox2.setGeometry(125, 125, 170, 25)
        self.textbox3.setGeometry(125, 170, 250, 25)
        self.textbox4.setGeometry(125, 215, 250, 25)

        self.btn = QPushButton('发送验证码', self)
        self.btn.clicked.connect(self.phone_test)
        self.count = 30
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.btn.setStyleSheet('QPushButton:hover{color:blue;}'
                               'QPushButton{background-color:lightskyblue;color:white;}'
                               'QPushButton{border-radius:10%}')
        self.btn.setGeometry(305, 125, 70, 20)
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

        self.button.clicked.connect(self.verification_code)

    def showmaximized(self):
        if self.maxButton.text() == '1':
            # 最大化
            self.maxButton.setText('２')
            self.showMaximized()
        else:  # 还原
            self.maxButton.setText('1')
            self.showNormal()

    def phone_test(self):
        account = self.textbox1.text()
        phone = self.textbox2.text()
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        if account == '':
            reply = QMessageBox.question(self, '本程序', '请输入账号', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.show()
        else:
            res = re.search(phone_pat, phone)
            if res:
                # do_forget.code = ''.join(str(i) for i in R.sample(range(1, 10), 4))
                ma = dxyz(phone)
                do_forget.code = ma
                print(do_forget.code)
                if self.btn.isEnabled():
                    self.time.start()
                    self.btn.setEnabled(False)
            else:
                QMessageBox.question(self, '本程序', '请输入正确手机号', QMessageBox.Yes)

    def Refresh(self):
        if self.count > 0:
            self.btn.setText(str(self.count) + '秒后重发')
            self.count -= 1
        else:
            self.time.stop()
            self.btn.setEnabled(True)
            self.btn.setText('发送验证码')
            self.textbox2.clear()
            self.count = 30

    def verification_code(self):
        account = self.textbox1.text()
        phone = self.textbox2.text()
        input_code = self.textbox3.text()
        password = self.textbox4.text()

        if input_code == do_forget.code:
        # data = 'OK'
            data = do_forgetpwd(account, password, phone, self.s)
            print(data)
            if data == 'NO':
                QMessageBox.question(self, '本程序', '账号或手机号错误', QMessageBox.Yes)
                self.textbox1.clear()
                self.textbox3.clear()
                self.textbox4.clear()

            elif data == "OK":
                print('1')
                QMessageBox.question(self, '本程序', '绑定成功', QMessageBox.Yes)
                self.signalCall()
                print('绑定成功')
            elif data == 'Fall':
                print('失败')
                QMessageBox.question(self, '本程序', '未知因素绑定失败', QMessageBox.Yes)
            # self.button2.chicked.connect(self.signalCall)
        else:
            QMessageBox.question(self, '本程序', '验证码错误', QMessageBox.Yes)

    def signalCall(self):
        from xiugaimima import child1_window
        from qq_main import main_window
        self.a = main_window(self.s)
        self.cp = child1_window(self.s)  # 修改密码
        self.d = child2_window(self.s)  # 注册
        self.f = do_forget(self.s)
        self.e = update_phone(self.s)

        self.a.button.clicked.connect(self.a.signalCall)
        self.a.button1.clicked.connect(self.cp.show)
        self.a.button1.clicked.connect(self.a.close)
        self.a.button2.clicked.connect(self.d.show)
        self.a.button2.clicked.connect(self.a.close)
        self.a.btn.clicked.connect(self.e.show)
        self.a.btn.clicked.connect(self.a.close)
        self.a.btn1.clicked.connect(self.f.show)
        self.a.btn1.clicked.connect(self.a.close)

        self.cp.button1.clicked.connect(self.a.show)
        self.cp.button1.clicked.connect(self.cp.close)
        self.d.button1.clicked.connect(self.a.show)
        self.d.button1.clicked.connect(self.d.close)
        self.e.button1.clicked.connect(self.a.show)
        self.e.button1.clicked.connect(self.e.close)
        self.f.button1.clicked.connect(self.a.show)
        self.f.button1.clicked.connect(self.f.close)
        self.a.show()
        self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     a = do_forget()  # 登录界面
#     a.show()
#     sys.exit(app.exec_())
