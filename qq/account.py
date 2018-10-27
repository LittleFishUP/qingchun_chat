# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from chat_client import *
from xiugaimima import child1_window
from zhuce import child2_window
from duxin import *
from update_phone import update_phone
from do_forget import do_forget
import random as R
import sys
import re
import http.client
import urllib
import json
import string

from chat_client import *


class account(QDialog):
    code = ''

    def __init__(self, account, s):
        super().__init__()
        self.account = account
        self.s = s
        self.resize(450, 330)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('账号')
        self.account_UI()

    def account_UI(self):
        self.label1 = QLabel(self)
        self.label2 = QLabel(self,objectName='label2')
        self.label2.setText('__________________________________')
        self.label3 = QLabel(self,objectName='label2')
        self.label3.setText('_________________')

        self.label1.setPixmap(QPixmap('timg1.jpg'))
        self.label1.setScaledContents(True)
        self.label1.setGeometry(0, 0, 450, 330)
        self.label = QLabel(self)
        self.label4 = QLabel(self)
        self.label.setGeometry(60, 40, 340, 260)
        self.label.setStyleSheet(
            'QLabel{background-color:rgba(255,255,255,0.5);border-radius:5%}')
        self.lable1 = QLabel(self)
        self.lable1.setGeometry(100, 90, 250, 50)
        self.label2.setGeometry(100, 130, 250, 50)
        self.label3.setGeometry(100, 180, 250, 50)
        self.label4.setGeometry(100,50,80,30)
        self.lable1.setText('绑定手机,忘记密码可快速修改')
        self.label4.setText('账号:')
        self.label4.setStyleSheet(
            'QLabel{font-size:24px;color:red;}')

        self.textbox1 = QLineEdit(self)
        self.textbox1.setFrame(False)
        self.textbox1.setText(self.account)
        self.textbox2 = QLineEdit(self)
        self.textbox3 = QLineEdit(self)
        self.textbox1.setGeometry(180, 50, 250, 30)
        self.textbox2.setGeometry(100, 130, 180, 30)
        self.textbox3.setGeometry(100, 180, 80, 40)
        self.textbox1.setStyleSheet("QLineEdit{background-color:rgba(255,255,255,0);}"
                                    "QLineEdit{font-size:30px;color:red;}"
                                    )
        self.textbox2.setStyleSheet("QLineEdit{border:none;background-color:rgba(255,255,255,0);font-size:22px;}"
                                    "QLineEdit{color:green}"
                                    "QLineEdit:hover{color:red}"
                                    # "QLineEdit:{selection-color: green;}"
                                    )
        self.textbox3.setStyleSheet("QLineEdit{border:none;background-color:rgba(255,255,255,0);font-size:22px;}"
                                    "QLineEdit{color:green}"
                                    "QLineEdit:hover{color:red}"
                                    )

        self.button1 = QPushButton('发送验证码', self)
        self.button2 = QPushButton('完成', self)
        self.button3 = QPushButton('返回登录', self)
        self.button1.setGeometry(300, 130, 70, 30)
        self.button2.setGeometry(210, 180, 50, 30)
        self.button3.setGeometry(100, 240, 100, 40)
        self.button1.setStyleSheet('QPushButton{background-color:lightskyblue;color:white;border-radius:5%;font-size:13px;}'
                                   'QPushButton:hover{color:blue}')
        self.button2.setStyleSheet('QPushButton{background-color:lightskyblue;color:white;border-radius:5%;font-size:18px;}'
                                   'QPushButton:hover{color:blue}')
        self.button3.setStyleSheet('QPushButton{background-color:lightskyblue;color:white;border-radius:5%;font-size:18px;}'
                                   'QPushButton:hover{color:blue}')
        self.button1.clicked.connect(self.phone_test)
        self.count = 30
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.button2.clicked.connect(self.verification_code)
        self.button3.clicked.connect(self.signalCall)

        self.minButton = QPushButton('0', self, objectName='min')
        self.minButton.setFont(QFont("Webdings"))
        # self.minButton.setIcon(QIcon(QPixmap('1.png')))
        self.minButton.clicked.connect(self.showMinimized)
        self.maxButton = QPushButton('1', self, objectName='max')
        self.maxButton.setFont(QFont("Webdings"))
        # self.maxButton.setIcon(QIcon(QPixmap('2.png')))
        self.maxButton.clicked.connect(self.showmaximized)
        self.closeButton = QPushButton('r', self, objectName='close')
        self.closeButton.setFont(QFont("Webdings"))
        # self.closeButton.setIcon(QIcon(QPixmap('4.png')))
        self.closeButton.clicked.connect(self.close)
        self.minButton.setGeometry(360, 0, 30, 30)
        self.maxButton.setGeometry(390, 0, 30, 30)
        self.closeButton.setGeometry(420, 0, 30, 30)
        self.setStyleSheet(
            'QPushButton{border:none;}#min:hover,#max:hover,#close:hover{background-color:red;}')

    def showmaximized(self):
        if self.maxButton.text() == '1':
            # 最大化
            self.maxButton.setText('２')
            self.showMaximized()
        else:  # 还原
            self.maxButton.setText('1')
            self.showNormal()

    def phone_test(self):
        phone = self.textbox2.text()
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, phone)
        if res:
            data = dxyz(phone)
            account.code = data
            print(data)
            if self.button1.isEnabled():
                self.time.start()
                self.button1.setEnabled(False)
            # data = add_phone(phone, self.account, self.s)
            # if data == "Fall":
            #     QMessageBox.question(self, '本程序', '绑定失败', QMessageBox.Yes)
        else:
            QMessageBox.question(self, '本程序', '请输入正确手机号', QMessageBox.Yes)

    def Refresh(self):
        if self.count > 0:
            self.button1.setText(str(self.count) + '秒后重发')
            self.count -= 1
        else:
            self.time.stop()
            self.button1.setEnabled(True)
            self.button1.setText('发送验证码')
            self.count = 30

    def verification_code(self):
        phone = self.textbox2.text()
        input_code = self.textbox3.text()
        # # j = 4
        # code = '1234'
        # # code = ''
        # code = ''.join(str(i) for i in R.sample(range(1,10),4))
        if input_code == account.code:
            # data = 'OK'
            data = add_phone(phone, self.account, self.s)
            if data == 'OK':
                QMessageBox.question(self, '本程序', '绑定成功', QMessageBox.Yes)
                self.signalCall()
            elif data == 'Fall':
                print('失败')
            # self.button2.chicked.connect(self.signalCall)
        else:
            print("验证码输入有误")

    def signalCall(self):
        from qq_main import main_window

        # self.button.clicked.connect(self.f.show)
        self.a = main_window(self.s)
        self.c = child1_window(self.s)
        self.d = child2_window(self.s)
        self.e = do_forget(self.s)
        self.f = account(self.account, self.s)
        self.g = update_phone(self.s)

        self.a.button.clicked.connect(self.a.signalCall)
        self.a.button1.clicked.connect(self.c.show)
        self.a.button1.clicked.connect(self.a.close)
        self.a.button2.clicked.connect(self.d.show)
        self.a.button2.clicked.connect(self.a.close)
        self.a.btn.clicked.connect(self.g.show)
        self.a.btn.clicked.connect(self.a.close)
        self.a.btn1.clicked.connect(self.e.show)
        self.a.btn1.clicked.connect(self.a.close)

        self.c.button1.clicked.connect(self.a.show)
        self.c.button1.clicked.connect(self.c.close)

        self.d.button1.clicked.connect(self.a.show)
        self.d.button1.clicked.connect(self.d.close)

        self.e.button1.clicked.connect(self.a.show)
        self.e.button1.clicked.connect(self.e.close)

        # self.f.button1.clicked.connect(self.a.show)
        # self.f.button1.clicked.connect(self.f.close)

        self.g.button1.clicked.connect(self.a.show)
        self.g.button1.clicked.connect(self.g.close)


        self.close()
        self.a.show()

    # def send_sms(self, text, mobile):
    #     host = "106.ihuyi.com"
    #     sms_send_uri = "/webservice/sms.php?method=Submit"
    #
    #     # APIID
    #     account = "C54090855"
    #     # APIKEY
    #     password = "eebfbd457f9bd4f0ff3c060934726dd2"
    #     params = urllib.parse.urlencode({'account': account, 'password': password,
    #                                      'content': text, 'mobile': mobile, 'format': 'json'})
    #     headers = {"Content-type": "application/x-www-form-urlencoded",
    #                "Accept": "text/plain"}
    #     conn = http.client.HTTPConnection(host, port=80, timeout=30)
    #     conn.request("POST", sms_send_uri, params, headers)
    #     response = conn.getresponse()
    #     response_str = response.read()
    #     conn.close()
    #     return response_str
    #
    # def myrandom(self, count=6):
    #     myList = list(string.digits)  # 指定要生成验证码的集合，数字，大小写字母
    #     # 在指定的mylist集合中随机取出count个集合
    #     lists = R.sample(myList, count)
    #     return "".join(lists)
    #
    # def dxyz(self, mobile):
    #     y = self.myrandom()
    #     mobile = str(mobile)
    #     text = "您的验证码是：{}。请不要把验证码泄露给其他人。".format(y)
    #     x = self.send_sms(text, mobile)
    #     a = json.loads(x)
    #     l = list(a.values())
    #     return (l[0], l[1], y)  # 返回码，返回内容，验证码
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     a = account('66666666','s')#登录界面
#     a.show()
#     sys.exit(app.exec_())
