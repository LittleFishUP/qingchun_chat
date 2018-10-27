#coding=utf-8

from PyQt5.QtWidgets import QApplication, QToolBox, QListView, QMenu, QAction, QInputDialog, QMessageBox,QDialog
from PyQt5.QtCore import Qt
from ListWidget import ListWidget
from PyQt5.QtGui import QIcon
import sys

class QQ(QToolBox,QDialog):
    def __init__(self,s,account):
        super(QQ,self).__init__()
        self.s = s
        self.account = account
        self.setWindowTitle('1806聊天室')
        self.setWindowFlags(Qt.Dialog)
        self.setMinimumSize(200,600)
        self.setWhatsThis('这个一个模拟QQ软件')
        self.setWindowIcon(QIcon('./res/log.ico'))
        pListWidget = ListWidget(self.s,self.account,'F')
        pListWidget1 = ListWidget(self.s,self.account,'G')

        dic_list = {'listwidget':pListWidget, 'groupname':"我的好友"}
        dic_list1 = {'listwidget':pListWidget1, 'groupname':"我的群"}
        pListWidget.setListMap(dic_list)
        pListWidget1.setListMap(dic_list1)
        self.addItem(pListWidget, "我的好友")
        self.addItem(pListWidget1,'我的群')
        # self.show()
    
    def contextMenuEvent(self, event):
        pmenu = QMenu(self)
        pAddGroupAct = QAction("添加分组", pmenu)
        pmenu.addAction(pAddGroupAct)
        pAddGroupAct.triggered.connect(self.addGroupSlot)
        pmenu.popup(self.mapToGlobal(event.pos()))
    
    def addGroupSlot(self):
        groupname = QInputDialog.getText(self, "输入分组名", "")
        if groupname[0] and groupname[1]: 
            pListWidget1 = ListWidget(self.s,self.account,'A')
            self.addItem(pListWidget1, groupname[0])
            dic_list = {'listwidget':pListWidget1, 'groupname':groupname[0]}
            pListWidget1.setListMap(dic_list)
        elif groupname[0] == '' and groupname[1]:
            QMessageBox.warning(self, "警告", "我说你没有填写分组名哦~！")


    def closeEvent(self, event):
        reply = QMessageBox.question(self,'本程序','是否退出本程序',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.s.send(b"E")
            event.accept()
        else:
            event.ignore()

# if __name__ =='__main__':
#     app = QApplication(sys.argv)
#     qq = QQ()
#     sys.exit(app.exec_())