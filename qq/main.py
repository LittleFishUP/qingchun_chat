# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5 import QtGui,QtCore,Qt,uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Ui_main import Ui_MainWindow
from chat_client import *
from PyQt5.QtNetwork import QUdpSocket, QHostInfo, QNetworkInterface, QAbstractSocket, QHostAddress
import json
from MyWeather import *
from tcpserver_widget import TcpS
from tcpclient_widget import TcpC


class MainWindow(QMainWindow, Ui_MainWindow):


    def __init__(self,s,account,chatList,name,icon,friendList,data,parent=None):
        super(MainWindow, self).__init__(parent)
        self.target = ''
        self.s = s
        self.account = account
        self.chatList = chatList
        self.name = name
        self.icon = icon
        self.friendList = friendList
        self.data = data
        self.change_n = 0  # 表情隐藏显示判断数
        self.jpg_n = 1
        self.setupUi(self)
        self.setImg()
        self.setList()
        self.fileName = ''
        self.item = None

        self.server = TcpS(self)
        self.server.sendFileName[str].connect(self.getFileName)


        #基本框架颜色ui
        self.frame.setStyleSheet("QFrame{background-color:#3598DB};")
        self.frame_2.setStyleSheet("QFrame#frame_2{background-color:rgba(0,0,0,0)};")
        self.textBrowser.setStyleSheet(
            "QTextBrowser{background-color:rgba(255,255,255,.8);border-style:outset;border-radius:10};")
        self.textEdit.setStyleSheet(
            "QTextEdit{background-color:rgba(255,255,255,.6);border-style:outset;border-radius:10px};")
        self.frame_5.setStyleSheet("QFrame{background-color:rgba(0,0,0,0)};")
        self.frame_6.setStyleSheet("QFrame{background-color:rgba(0,0,0,0)};")

        # 大背景
        self.setStyleSheet("QFrame#frame_3{border-image:url(./images/background.jpg)};")
        # 左侧背景ui
        self.frame_4.setStyleSheet(
            "QFrame#frame_4{border-image:url(./images/leftliaotian.jpg);border-radius:20px;};")  # 我的好友外框

        #右侧背景ui
        self.frame_3.setStyleSheet("QFrame{background-color:#F5F6F8};")
        #上方设置ui
        self.huanyin.setStyleSheet("QLabel{color:#FFFFFF};")
        self.tubiao.setStyleSheet("QLabel{border-image:url(./images/001.jpg);}")
        self.userimg.setStyleSheet("QLabel{border-image:url("+self.icon+");border-radius: 10px;}")
        self.username.setStyleSheet("QLabel{color:#FFFFFF};")
        self.username.setText(self.name)

        #天气按钮
        self.pushButton.setStyleSheet("QPushButton{border-image:url(./images/011.png)}QPushButton:pressed{border-image:\
              url(./images/012.png)}")

        self.pushButton_3.setStyleSheet("QPushButton{border-image:url(./images/timg.png)}QPushButton:pressed{border-image:\
              url(./images/timg1.png)}")

        self.pushButton_4.setStyleSheet("QPushButton{border-image:url(./images/send.png)}QPushButton:pressed{border-image:\
              url(./images/send_2.png)}")  # 发送按钮
        self.pushButton_5.setStyleSheet("QPushButton{border-image:url(./images/hudie.png)}QPushButton:pressed{border-image:\
               url(./images/hudie_1.png)}")  # 关闭按钮
        self.pushButton_6.setStyleSheet("QPushButton{border-image:url(./images/biaoqing.png);}QPushButton:pressed{border-image:\
               url(./images/biaoqing_2.png)}")  # 表情按钮
        self.pushButton_7.setStyleSheet("QPushButton{border-image:url(./images/film_1.jpg)}QPushButton:pressed{border-image:\
               url(./images/film_2.jpg)}")  # 文件按钮
        self.pushButton_2.setStyleSheet("QPushButton{border-image:url(./images/020.png)}")

        #聊天列表UI
        #self.listWidget.setStyleSheet("QListWidget{border-radius:20px;border-style:outset;};")
        self.listWidget.setIconSize(QSize(55, 55))
        self.listWidget.setStyleSheet("QListWidget::Item {height:55}"
            "QListWidget::Item::QFont {color:black};{text-align:center}"
            "QListWidget::Item::QIcon {border-radius:10px}"
            "QListWidget::Item:hover{background:rgba(255,250,250,0.3); }"
            "QListWidget::item:selected:!active{border-width:0px; rgba(255,250,250,0.3); }"
            "QListWidget{border-radius:20px;}"
            )
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.itemSelectionChanged.connect(self.getListitems)
        self.listWidget.itemDoubleClicked.connect(self.refreshUi)
        self.pushButton_3.clicked.connect(self.groupchat)
        #文件按钮功能
        self.pushButton_6.pressed.connect(self.changebiao)#表情按钮
        #表情按钮隐藏
        self.tableWidget.hide()

        ###隐藏窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.closebutton.setStyleSheet('QPushButton{border:none;}QPushButton:pressed{background-color:red;}')
        self.minbutton.setStyleSheet('QPushButton{border:none;}QPushButton:pressed{background-color:red;}')

        for i in range(6):
            self.tableWidget.setRowHeight(i, 60)
        for i in range(6):
            self.tableWidget.setColumnWidth(i, 60)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止用户修改图片
        self.tableWidget.verticalHeader().setVisible(False)#行头隐藏
        self.tableWidget.horizontalHeader().setVisible(False)#列头隐藏
        self.tableWidget.itemDoubleClicked.connect(self.showImg)

        self.data.getDataSignal.connect(self.getText)
        self.data.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showtime)
        self.timer.start()

    def showtime(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        self.time.setText("     " + text)

    def getListitems(self):
        return self.listWidget.selectedItems()

    def refreshUi(self):
        self.item = self.getListitems()[0]#记录聊天对象
        self.target = self.item.text()
        friendAccount = [obj['account'] for obj in self.friendList if obj['name'] == self.target][0]
        charRecord = ''
        with open('./qqFile/'+self.account+"_"+friendAccount+'.txt','rb') as f:
            while True:
                data = f.read(1024)
                if len(data) < 1024:
                    charRecord += data.decode()
                    break
                charRecord += data.decode()
        self.textBrowser.document().setHtml(charRecord)
        self.textBrowser.moveCursor(QTextCursor.End)

    def groupchat(self):#群聊
        self.item = None
        self.target = 'groupchat'
        charRecord = ''
        with open('./qqFile/'+'chat.txt', 'rb') as f:
            while True:
                data = f.read(1024)
                if len(data) < 1024:
                    charRecord += data.decode()
                    break
                charRecord += data.decode()
        self.textBrowser.document().setHtml(charRecord)
        self.textBrowser.moveCursor(QTextCursor.End)

    def setList(self):
        for target in self.chatList:
            item = QListWidgetItem()
            if 'group' in target['target']:
                continue
            font = QFont()
            font.setPointSize(16)
            item.setFont(font)
            item.setIcon(target['icon'])
            item.setText(target['target'])
            self.listWidget.addItem(item)

    def getTableitems(self):
        return self.tableWidget.selectedItems()


    def getText(self,msg):
        dic = json.loads(msg)
        ipAddress = self.getIP()
        if dic['type'] == 'cg':
            if self.item == None:
                self.textBrowser.append(dic['msg'])
                self.textBrowser.moveCursor(QTextCursor.End)
        elif dic['type'] == 'cp':
            if self.item != None:
                if dic['froms'] == self.item.text():
                    self.textBrowser.append(dic['msg'])
                    self.textBrowser.moveCursor(QTextCursor.End)
        elif dic['type'] == 'S':#接收文件信息
            self.hasPendingFile(dic,ipAddress)


    def fileMsg(self,msg):
        time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.textBrowser.setTextColor(Qt.blue)
        self.textBrowser.setCurrentFont(QFont("Times New Roman", 12))
        self.textBrowser.append("[" + self.name + "]" + time)
        self.textBrowser.append(msg)
        self.textBrowser.moveCursor(QTextCursor.End)

    def showImg(self):
        from chat_client import chat
        item = self.getTableitems()[0]
        time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        if not item:
            print('图片出错')
        else:
            self.textBrowser.setTextColor(Qt.blue)
            self.textBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.textBrowser.append("[" + self.name + "]" + time)
            img = "<img src = './images/mao/" + item.text() + ".jpg' width='100' height='100'/>"
            self.textBrowser.append(img)
            self.textBrowser.moveCursor(QTextCursor.End)
            msg = "<p style='color: blue'>" + "[" + self.name + "]" + time + "</p>" + "<p>" + img + "</p>"
            chat(self.target, self.s, self.account, msg)
            print("触发成功")

    def setImg(self):
        for row in range(6):
            for col in range(6):
                icon = QTableWidgetItem(QIcon("./images/mao/%s.jpg" % self.jpg_n), str(self.jpg_n))
                self.tableWidget.setIconSize(QSize(50, 50))
                self.tableWidget.setItem(row, col, icon)
                self.jpg_n += 1

    #打开表情列表(隐藏或是显示)
    def changebiao(self):
        if self.change_n==0:
            self.tableWidget.show()
            self.change_n+=1
        elif self.change_n ==1:
            self.tableWidget.hide()
            self.change_n=0


    def hasPendingFile(self, dic,clientAddress):
        ipAddress = self.getIP()
        serverAddress = dic['ipAddress']
        if ipAddress == clientAddress:
            isreceive = "来自{}的文件：{}，是否接收？".format(dic['name'], dic['filename'])
            btn = QMessageBox.information(self, "接收文件", isreceive, QMessageBox.Yes, QMessageBox.No)
            if btn == QMessageBox.Yes:
                name = QFileDialog.getSaveFileName(self, "保存文件", dic['filename'])
                if name[0]:
                    client = TcpC(self)
                    client.setFileName(name[0])
                    client.setHostAddress(QHostAddress(serverAddress))
                    client.exec()


    def getFileName(self, name):
        """
        待传输文件的文件名
        """
        self.fileName = name
        self.sendFile()

    def sendFile(self):
        """
        发送文件信息给服务器
        """
        ipAddress = self.getIP()
        data = {'type':'S','filename':self.fileName,'account':self.account,'name':self.name,'target':self.target,'ipAddress':ipAddress}
        dataStr = json.dumps(data)
        self.s.send(dataStr.encode())

    def getIP(self):
        """
        获得用户IP
        """
        addressList = QNetworkInterface.allAddresses()
        for address in addressList:
            if address.protocol() == QAbstractSocket.IPv4Protocol and address != QHostAddress.LocalHost and address.toString()[:3] != "169" and address.toString().split(".")[-1] != "1":
                return address.toString()
        return "0.0.0.0"
    
    def sendMessage(self):
        from chat_client import chat
        msg = self.getMessage()
        if msg:
            time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            self.textBrowser.setTextColor(Qt.blue)
            self.textBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.textBrowser.moveCursor(QTextCursor.End)
            self.textBrowser.append("<span style = 'color: blue'>[" + self.name + "]" + time+"<span>")
            self.textBrowser.append(msg)
            self.textBrowser.moveCursor(QTextCursor.End)
            msg = "<p style='color: blue'>[" + self.name + "]" + time+"</p>"+ msg
            chat(self.target,self.s,self.account,msg)


    #发送窗口
    def getMessage(self):
        msg = self.textEdit.toHtml()
        if self.textEdit.toPlainText() == "":
            QMessageBox.warning(self, "警告", "发送内容不能为空", QMessageBox.Ok)
            return
        self.textEdit.clear()
        self.textEdit.setFocus()
        return msg

    def mergeFormatDocumentOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def weather(self):
        myshow = myWeather()
        myshow.show()


    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.s.send(b'QT')
        self.data.quit()
        self.timer.stop()
        self.hide()

    @pyqtSlot(bool)
    def on_colorToolBtn_clicked(self):
        '''
        设置字体颜色
        :param p0:
        :return:
        '''
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatDocumentOrSelection(fmt)
        self.textEdit.setFocus()

    @pyqtSlot(str)
    def on_SizeComboBox_currentIndexChanged(self, p0):
        '''
        设置字体大小
        :param p0:
        :return:
        '''
        fmt = QTextCharFormat()
        fmt.setFontPointSize(int(p0))
        self.mergeFormatDocumentOrSelection(fmt)
        self.textEdit.setFocus()

    @pyqtSlot(str)
    def on_fontComboBox_currentIndexChanged(self, p0):
        '''
        设置字体
        :param p0:
        :return:
        '''
        fmt = QTextCharFormat()
        fmt.setFontFamily(p0)
        self.mergeFormatDocumentOrSelection(fmt)
        self.textEdit.setFocus()

    @pyqtSlot()
    def on_pushButton_4_clicked(self):#发送按钮
        '''
        发送聊天信息
        :return:
        '''
        self.sendMessage()


    @pyqtSlot()
    def on_pushButton_clicked(self):
        '''
        查看天气
        :return:
        '''
        self.weather()


    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        """
        选择文件发送对象
        """
        userlist = self.getListitems()
        if not (userlist):
            QMessageBox.warning(self, "选择用户", "请先从用户列表选择要传送的用户!", QMessageBox.Ok)
            return
        else:
            self.server.exec()

#重写函数类
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

# if __name__ == "__main__":
#
#     app = QtWidgets.QApplication(sys.argv)
#     QApplication.processEvents()
#
#     ui = MainWindow()
#
#     ui.show()
#     sys.exit(app.exec_())
