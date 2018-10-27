#coding=utf-8
# import sys
# sys.path.append(".")
from PyQt5.QtCore import *

from Add_group import Dialog_additem1
from Dialog_additem import Dialog_additem
from chat_client import *
from main import *


class ListWidget(QListWidget):
    startSignal = pyqtSignal()
    map_listwidget = []


    def __init__(self,s,account,msg):
        super().__init__()
        self.s = s
        self.msg = msg
        self.account = account
        self.chatList = []
        self.Data_init(self.msg)
        self.Ui_init()
        self.data = getdata(self.s)
        # self.data.getDataSignal.connect(getText)
        # self.data.start()


    def Data_init(self,msg):
        if msg == 'F':#好友列表
            self.delAllItemSlot()
            self.myself(self.s,self.account)
            self.getFriend(self.s,self.account)
        if msg == 'G':#群列表
            self.getGroups(self.s,self.account)
        if msg == 'A':#创建列表
            item = QListWidgetItem()
            self.addItem(item)


    def Ui_init(self):
        self.setIconSize(QSize(70,70))
        self.setStyleSheet("QListWidget{background-image:url('./img/timg.jpg');border:0px solid gray;color:white;}"
                           "QListWidget::Item{padding-top:0px; padding-bottom:4px;background-color:rgba(255,255,255,0)}"
                           "QListWidget::Item:hover{background:rgba(255,250,250,0.3); }"
                           "QListWidget::item:selected:!active{border-width:0px; rgba(255,250,250,0.3); }"
                           )
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemSelectionChanged.connect(self.getListitems)
        self.itemDoubleClicked.connect(self.clicked)
    
    def getListitems(self):
        return self.selectedItems()

    def clicked(self):
        items = self.getListitems()
        if self is self.find('我的好友'):
            target = items[0].text()
            icon = items[0].icon()
            targetMsg = {'target':target,'icon':icon}
            if not (targetMsg['target'] in [obj['target'] for obj in self.chatList]):
                self.chatList.append(targetMsg)
            self.handel()
            print('触发好友'+target)
        elif self is self.find('我的群'):
            target = 'group'+items[0].text()
            icon = items[0].icon()
            targetMsg = {'target': target, 'icon': icon}
            if not (targetMsg in [obj['target'] for obj in self.chatList]):
                self.chatList.append(targetMsg)
            self.handel()
            print("触发群"+target)


    def handel(self):
        self.ui = MainWindow(self.s,self.account,self.chatList,self.name,self.icon,self.friendList,self.data)
        self.ui.show()


    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)

            if self is self.find('我的好友'):
                pAddItem = QAction("添加好友",pmenu)
                pmenu.addAction(pAddItem)
                pAddItem.triggered.connect(self.addItemSlot)

                pReFresh = QAction('刷新', pmenu)
                pmenu.addAction(pReFresh)
                pReFresh.triggered.connect(self.reFresh)

                pDeleteAct = QAction("删除", pmenu)
                pmenu.addAction(pDeleteAct)
                pDeleteAct.triggered.connect(self.deleteItemSlot)

                if len(self.map_listwidget) > 2:
                    pSubMenu = QMenu("转移联系人至" ,pmenu)
                    pmenu.addMenu(pSubMenu)
                    for item_dic in self.map_listwidget:
                        if item_dic['listwidget'] is not self and (item_dic['listwidget'] != "我的群"):
                            pMoveAct = QAction(item_dic['groupname'] ,pmenu)
                            pSubMenu.addAction(pMoveAct)
                            pMoveAct.triggered.connect(self.move)

            if self is self.find('我的群'):
                pAddGroupItem = QAction('添加群',pmenu)
                pmenu.addAction(pAddGroupItem)
                pAddGroupItem.triggered.connect(self.addgroup)

                pSetGroupItem = QAction('创建群', pmenu)
                pmenu.addAction(pSetGroupItem)
                pSetGroupItem.triggered.connect(self.setgroup)

                pReFreshGroup = QAction('刷新', pmenu)
                pmenu.addAction(pReFreshGroup)
                pReFreshGroup.triggered.connect(self.reFreshGroup)

            pmenu.popup(self.mapToGlobal(event.pos()))
    
    def deleteItemSlot(self):
        dellist = self.getListitems()
        for delitem in dellist:
            name = delitem.text()#昵称
            msg = delFriend(self.s,self.account,name)
            if msg == 'OK':
                del_item = self.takeItem(self.row(delitem))
                del del_item
                print("好友删除成功")
            else:
                print("删除好友失败")

    def setgroup(self):#创建群
        m = Dialog_additem1()
        r = m.exec()
        if r > 0:
            groupName = m.lineEdit.text()
            data = setGroup(self.s,self.account,groupName)
            if data == "OK":
                f1 = open('./qqFile/' + groupName + '.txt', 'w')
                f1.close()
                print("创建群成功")
            else:
                print("创建群失败")

    def addgroup(self):#加入群
        dg = Dialog_additem1()
        r = dg.exec()
        if r > 0:
            groupName = dg.lineEdit.text()
            data = addGroup(self.s,groupName,self.account)
            if data == "OK":
                print("加入群成功")
            else:
                print("加入群失败")


    def reFresh(self):#刷新好友列表
        self.delAllItemSlot()
        self.myself(self.s, self.account)
        self.getFriend(self.s,self.account)

    def reFreshGroup(self):#刷新群组列表
        self.delAllItemSlot()
        self.getGroups(self.s,self.account)


    def delAllItemSlot(self):#删除所有item对象
        count = self.count()
        for i in range(0,count):
            item = self.takeItem(0)
            del item


    def addItemSlot(self):#添加好友
        dg = Dialog_additem()
        r = dg.exec()
        if r > 0:
            item = QListWidgetItem()
            friendAccount = dg.lineEdit.text()
            data = addFriends(self.s,self.account,friendAccount)
            if data:
                font = QFont()
                font.setPointSize(16)
                item.setFont(font)
                item.setText(data[0])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setIcon(QIcon("./res/"+data[1]))
                self.addItem(item)
                f1 = open('./qqFile/'+self.account+'_'+friendAccount+'.txt','w')
                f2 = open('./qqFile/'+friendAccount+'_'+self.account+'.txt','w')
                f1.close()
                f2.close()
            else:
                print('好友添加失败')

    def setListMap(self, listwidget):
        self.map_listwidget.append(listwidget)

    def move(self):
        tolistwidget = self.find(self.sender().text())
        movelist = self.getListitems()
        for moveitem in movelist:
            pItem = self.takeItem(self.row(moveitem))
            tolistwidget.addItem(pItem)

    def find(self, pmenuname):
        for item_dic in self.map_listwidget:
            if item_dic['groupname'] == pmenuname:
                return item_dic['listwidget']

    def myself(self,s,account):
        my = getMyself(s,account)
        self.icon = "./res/" + my[1]
        self.name = my[0]
        item = QListWidgetItem()
        font = QFont()
        font.setPointSize(16)
        item.setFont(font)
        item.setText(self.name)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setIcon(QIcon(self.icon))
        item.setForeground(QBrush(Qt.red))
        item.setToolTip("在线")
        self.addItem(item)

    def getFriend(self,s,account):#获取好友列表
        self.friendList = getFriends(s, account)
        if self.friendList == None:
            item = QListWidgetItem()
            self.addItem(item)
        else:
            for obj in self.friendList:
                icon = "./res/" + obj['img']
                name = obj['name']
                flag = obj['flag']
                item = QListWidgetItem()
                font = QFont()
                font.setPointSize(16)
                item.setFont(font)
                item.setText(name)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setIcon(QIcon(icon))
                if flag == '1':
                    item.setForeground(QBrush(Qt.red))
                    item.setToolTip("在线")
                self.addItem(item)

    def getGroups(self,s,account):#获取群列表
        groups = getGroup(s,account)
        if groups == None:
            item = QListWidgetItem()
            self.addItem(item)
        else:
            for obj in groups:
                icon = "./res/" + obj['img']
                groupName = obj['groupName']
                item = QListWidgetItem()
                font = QFont()
                font.setPointSize(16)
                item.setFont(font)
                item.setText(groupName)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setIcon(QIcon(icon))
                self.addItem(item)
