import threading, sys, json, re

from PyQt5.QtCore import pyqtSignal, QThread
from main import *
import platform,os
myre = r"^[_a-zA-Z]\w{0,}"

#
# class inputdata(threading.Thread):
#     def __init__(self,name,account,s,msg):
#         threading.Thread.__init__(self)
#         self.name = name
#         self.account = account
#         self.s = s
#         self.msg = msg
#
#     # 用户输入选择然后执行不同的功能程序
#     def run(self):
#       #   menu = """
#       # (CP):　个人聊天
#       # (CG): 进入群聊
#       # (AG): 添加群
#       # (EG): 入群
#       # (H): 菜单帮助
#       # (Q): 退出系统
#       # """
#       #   print(menu)
#       #   while True:
#       #       operation = input('操作("h"): ')
#             if self.msg in 'cPCPCpcp':
#                 # 进入个人聊天
#                 target = input('选择好友: ')
#                 chat(target,self.name,self.s,self.account)
#                 # continue
#
#             if self.msg in 'cgCGCgcG':
#                 # 进入群聊
#                 target = input('选择群: ')
#                 chat('group'+target,self.name,self.s,self.account)
#                 # continue
#             # if self.msg in 'agAGAgaG':
#             #     # 添加群组
#             #     groupName = addGroup()
#             #     if groupName:
#             #         dataObj = {'type': 'ag', 'groupName': groupName,'name':self.name,'account':self.account}
#             #         dataObj = json.dumps(dataObj)
#             #         self.s.send(dataObj.encode('utf-8'))
#                 # continue
#
#             # if self.msg in 'egEGEgeG':
#             #     # 入群
#             #     groupname = input('输入群名字: ')
#             #     if not re.findall(myre, groupname):
#             #         print('群名称不合法!')
#             #         return None
#             #     dataObj = {'type': 'eg', 'groupName': groupname,'name':self.name,'account':self.account}
#             #     dataObj = json.dumps(dataObj)
#             #     self.s.send(dataObj.encode('utf-8'))
#                 # continue
#             # if operation in 'hH':
#                 # print(menu)
#                 # continue
#
#             # if self.msg in 'qQ':
#             #     self.s.send(b'q')
#             #     sys.exit(1)
#             # else:
#             #     print('没有该操作!')


class getdata(QThread):
    getDataSignal = pyqtSignal(str)
    getFileSignal = pyqtSignal(str)
    def __init__(self,s):
        super(getdata,self).__init__()
        self.s = s

    # 接收数据线程
    def run(self):
        isRUn = True
        while isRUn:
            data = self.s.recv(4096).decode('utf-8')
            # print(1)
            dataList = data.split('$')
            if data == 'QT':
                isRUn = False
            # elif data[0] == 'S':
            #     msg = data[2:]
            #     msgDit = json.loads(msg)
            #     filename = msgDit['filename']
            #     # fileMsg = msgDit['fileMsg']
            #
            #     fileMsg = b''
            #     while True:  # 接收文件数据
            #         fileRecv = self.s.recv(1024)
            #         if len(fileRecv) < 1024:
            #             fileMsg += fileRecv
            #             break
            #         fileMsg += fileRecv
            #     print(fileMsg)
            #     flag = self.UsePlatform(filename,fileMsg)
            #     # sendMsg = ''
            #     if flag:
            #         sendMsg = "文件"+filename+"接收成功"
            #     else:
            #         sendMsg = "文件" + filename + "接收失败"
            #     self.getFileSignal.emit(sendMsg)
            else:
                for dataObj in dataList:
                    if dataObj:
                        # print(dataObj)
                        msg = json.loads(dataObj)

                        if msg['type'] == 'cg':
                            try:
                                f = open('./qqFile/'+msg['groupName']+'.txt','ab')
                            except:
                                print('打开文件失败')
                            else:
                                f.write(("<p>"+msg['msg']+"</p>").encode())
                                f.close()
                            # try:
                            #     f1 = open('./qqFile/'+dataObj['groupName']+'.txt', 'rb')
                            # except:
                            #     print('打开文件失败')
                            # else:
                            #     data = ''
                            #     while True:
                            #         msg = f1.read(1024).decode()
                            #         if not msg:
                            #             break
                            #         data += msg
                            self.getDataSignal.emit(dataObj)
                        elif msg['type'] == 'S':
                            self.getDataSignal.emit(dataObj)
                        else:
                            try:
                                f = open('./qqFile/'+msg['account']+"_"+msg['friendAccount']+'.txt','ab')
                                f1 = open('./qqFile/' + msg['friendAccount'] + "_" + msg['account'] + '.txt', 'ab')
                            except:
                                print('打开文件失败')
                            else:
                                if "img" in msg['msg']:
                                    f.write(("<p>"+msg['msg']+"</p>").encode())
                                    f1.write(("<p>" + msg['msg'] + "</p>").encode())
                                else:
                                    f.write((msg['msg']).encode())
                                    f1.write((msg['msg']).encode())
                                f.close()
                                f1.close()
                            self.getDataSignal.emit(dataObj)



def add_phone(phone, count, s):
    msg = "P {} {}".format(phone, count)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        return 'OK'
    else:
        return "Fall"

def update_phone1(account,passwd,phone,s):
    msg = "U {} {} {}".format(account, passwd, phone)
    s.send(msg.encode())
    data = s.recv(128).decode()
    return data

def do_forgetpwd(account, passwd, phone, s):
    msg = "W {} {} {}".format(account, passwd, phone)
    s.send(msg.encode())
    data = s.recv(128).decode()
    return data


def chat(target,s,account,msg):
    if len(msg) > 0 and not (msg in 'qQ'):
        groupName = ''
        if 'group' in target:
            optype = 'cg'
            groupName = target[5::]
        else:
            optype = 'cp'
        dataObj = {'type': optype, 'to': target, 'msg': msg, 'account':account,'groupName':groupName}
        datastr = json.dumps(dataObj)
        s.send(datastr.encode())

def addGroup(s,groupname,account):#加入群
    if not re.findall(myre, groupname):
        print('群名称不合法!')
        return None
    dataObj = {'type': 'eg', 'groupName': groupname,  'account': account}
    dataObj = json.dumps(dataObj)
    s.send(dataObj.encode('utf-8'))
    msg = s.recv(4096).decode()
    return msg


def setGroup(s,account,groupName):#创建群
    dataObj = {'type': 'ag', 'groupName': groupName, 'account':account}
    dataObj = json.dumps(dataObj)
    s.send(dataObj.encode('utf-8'))
    msg = s.recv(1024).decode()
    return msg

def do_register(account,passwd,name,s):
        msg = "R {} {} {}".format(account,passwd,name)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return name
        elif data == 'EXISTS':
            print('用户已经存在')
            return "Exists"
        elif data == 'RN':
            print('昵称已存在')
            return 'RN'
        else:
            return "Fall"


def do_login(account,passwd,s):
    msg = "L {} {}".format(account,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        name = s.recv(1024).decode()
        return account,name
    elif data == 'IN':
        print('已经在线')
        return 1,1
    else:
        print("密码错误")
        return 1,1

def delFriend(s,account,friendName):
    msg = "D " + account + " " + friendName
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == "OK":
        print("删除好友成功")
    else:
        print("删除好友失败")
    return data


def getMyself(s,account):
    msg = 'Y '+account
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data != 'N':
        return data.split(' ')
    else:
        print('获取失败')



def addFriends(s,account,friend):
    msg = "F " + account + " " + friend
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if "OK" in data:
        print("添加好友成功")
        return data.split(' ')[1:]
    elif data == "IN":
        print("你们已经是好友了")
        return None
    elif data == "NI":
        print("对方不存在")
        return None
    elif data == "NC":
        print("对方不在线")
        return None
    else:
        print("添加好友失败")
        return None

def sendFile(s,filePath,target,filename):
    global f
    try:
        dit = {'target': target, 'filename': filename}
        msg = "S " + json.dumps(dit)
        s.sendall(msg.encode())

        f = open(filePath,'rb')
        # fileMsg = b''
        while True:
            data = f.read(1024)
            print(data)
            if len(data)<1024:
                s.send(data)
                break
            s.send(data)


    except IOError as e:
        print(e)
        print('发送失败')
    finally:
        f.close()



def change_passwd(account,passwd,newpasswd,s):
    dataobj = {'type':'np','account':account,'passwd':passwd,'newpasswd':newpasswd}
    datastr = json.dumps(dataobj)
    s.sendall(datastr.encode())
    data = s.recv(1024).decode()
    return data

def getGroup(s,account):#获取群信息
    msg = 'G '+account
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'N':
        print('你没有加入任何群')
        return None
    else:
        dataList = data.split('#')
        groupList = []
        for obj in dataList:
            if obj == '':
                break
            msg1 = json.loads(obj)
            groupList.append(msg1)
        return groupList


def getFriends(s,account):#获取好友列表以及在线好友
    msg = 'M '+account
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'N':
        print('你没有好友')
        return None
    else:
        dataList = data.split('#')
        friendList = []
        for obj in dataList:
            if obj == '':
                break
            msg = json.loads(obj)
            friendList.append(msg)
        return friendList


