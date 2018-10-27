from group import Ui_Dialog1
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

class Dialog_additem1(QDialog, Ui_Dialog1):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog_additem1, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(300, 150)
        self.flag = False  # 判断返回的联系人图标是默认的还是自定义的
        self.iconpath = ''

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self, '提示', '群名称不能为空')
            self.lineEdit.setFocus()
        else:
            self.done(1)  # 给主窗口的返回值

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.done(-1)  # 给主窗口的返回值

    def geticonpath(self):
        if self.flag == True:
            return self.iconpath
        else:
            return "./res/default.ico"


