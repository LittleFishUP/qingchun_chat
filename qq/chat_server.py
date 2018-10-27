import json
import socketserver
import time
from random import randint

from mysqlpython import *

db = Mysqlpython('qq_chat')

connLst = []#记录在线人
groupLst = []#记录群号

DIR_PATH = "/home/tarena/"


class Connector(object): ##在线对象类
    def __init__(self,account,password,name,addrPort,conObj,img):
        self.account = account
        self.password = password
        self.name = name
        self.addrPort = addrPort#端口号
        self.conObj = conObj#套接字
        self.img = img


class Group(object):#群组类
    def __init__(self,groupname,groupOwner):
        self.groupId = 'group'+str(len(groupLst)+1)
        self.groupName = 'group'+groupname
        self.groupOwner = groupOwner
        self.createTime = time.time()
        self.members=[groupOwner]

def do_register(s,data):
    l = data.split(' ')
    account = l[1]
    passwd = l[2]
    name = l[3]

    sql = "select * from user where account = %s"#判断账号是否存在
    r = db.all(sql,[account])
    if len(r) != 0:
        s.send(b'EXISTS')
        return

    sql = "select name from user where name = %s;"#判断昵称是否存在
    r = db.all(sql,[account])
    if len(r) != 0:
        s.send(b'RN')
        return

    img = str(randint(0,26))+".jpg"
    sql = "insert into user (account,passwd,name,img) values (%s,%s,%s,%s)"
    try:
        db.zhixing(sql,[account,passwd,name,img])
        s.send(b'OK')
    except:
        db.rollback()
        s.send(b'FALL')
        return
    else:
        print('注册成功')


def do_login(s,data,addr):
    l = data.split(' ')
    account = l[1]
    passwd = l[2]
    for i in connLst:
        if i.account == account:
            s.send(b"IN")
            return
    sql = "select name,img from user where account = %s and passwd = %s"
    r = db.all(sql,l[1:3])
    if len(r) == 0:
        s.send('Not'.encode())
        return
    else:

        s.send(b'OK')
        time.sleep(0.1)
        s.send(r[0][0].encode())
        connObj = Connector(account,passwd,r[0][0],addr,s,r[0][1])#添加到在线列表中
        connLst.append(connObj)


def do_friend(s,data):
    l = data.split(' ')
    account = l[1]
    friendAccount = l[2]
    sql = "select account,name,img from user where account = %s"
    r = db.all(sql,[friendAccount])
    if len(r) == 0:#判断好友是否存在
        s.send(b'NI')
        return
    friendIco = r[0][2]
    name = r[0][1]
    for i in connLst:#判断是否在线
        if i.account == friendAccount:
            sql = "select f_account from friend where account = %s"
            r = db.all(sql, [account])
            for i in r:#判断是否已经是好友
                if i[0] == friendAccount:
                    s.send("IN".encode())
                    break
            else:
                sql = "insert into friend (account,f_account) values(%s,%s)"
                try:
                    db.zhixing(sql, l[1:3])
                    db.zhixing(sql,l[2:0:-1])
                    msg = 'OK '+name+" "+friendIco
                    s.send(msg.encode())
                except:
                    db.rollback()
                    s.send(b'FALL')
            break
    else:
        s.send(b"NC")


def add_phone(s, data):
    l = data.split(' ')
    iphone = l[1]
    count = l[2]
    sql = "update user set phone=%s where account=%s"
    try:
        db.zhixing(sql, [iphone, count])
        s.send(b'OK')
    except:
        db.rollback()
        s.send(b'FALL')
        return


def update_phone(s,data):
    l = data.split(' ')
    account = l[1]
    password = l[2]
    iphone = l[3]
    sql = 'select name from user where account = %s and passwd = %s'
    r = db.all(sql,[account,password])
    if len(r)  == 0:
        s.send(b'NO')
        return
    else:
        sql1 = 'update user set phone = %s where account = %s and passwd = %s'
        try:
            db.zhixing(sql1, [iphone,account,password])
            s.send(b'OK')
        except:
            db.rollback()
            s.send(b'FALL')
        return


def do_forget(s, data):
    l = data.split(' ')
    account = l[1]
    newpasswd = l[2]
    iphone = l[3]
    sql = "select name from user where account = %s and phone = %s"
    r = db.all(sql, [account, iphone])

    if len(r) == 0:
        s.send(b'NO')
        return
    else:
        sql1 = "update user set passwd=%s where account=%s and phone=%s"
        try:
            db.zhixing(sql1, [newpasswd, account, iphone])
            s.send(b'OK')
        except:
            db.rollback()
            s.send(b'FALL')
        return


def send_file(s,data):
    '''
    将文件信息发给接收人
    '''
    dataDit = json.loads(data)
    for i in connLst:  # 获取在线人的套接字
        if i.name == dataDit['target']:
            data+='$'
            print(data)
            i.conObj.sendall(data.encode())


def do_del_friend(s,data):
    l = data.split(' ')
    account = l[1]
    friendName = l[2]
    sql = "select account from user where name = %s;"#获取好友账号
    r = db.all(sql,[friendName])
    friendAccount = r[0][0]

    sql = "select f_account from friend where account = %s"
    r = db.all(sql, [account])
    for i in r:
        if i[0] == friendAccount:
            sql = "delete from friend where account = %s and f_account = %s"
            try:
                db.zhixing(sql, [account,friendAccount])
                db.zhixing(sql, [friendAccount,account])
                s.send(b'OK')
                break
            except:
                db.rollback()
                s.send(b'FALL')


def do_chat(s,dataobj,data):
    l = []#在线人的账号
    # f1 = open('132_mmm.txt','ab')
    # s1 = f1.read()
    # f1.close()
    # print(s1)
    for obj in connLst:
        l.append(obj.account)
    sql = "select name from user where account = %s"
    r = db.all(sql,[dataobj['account']])
    name = r[0][0]
    if dataobj['type'] == 'cg':
        # 群内广播（除发消息的人）
        sql = "select member from groupMember where groupName = %s"
        r = db.all(sql,[dataobj['groupName']])
        # print(connLst)
        for obj in r:
            if obj[0] != dataobj['account']:#不发给自己
                # print(1)
                # if obj[0] in l:#在线
                for i in connLst:#获取在线人的套接字
                    if i.account == obj[0]:
                        dataobj['froms'] = name
                        data = json.dumps(dataobj)
                        i.conObj.sendall(data.encode())
    elif dataobj['type'] == "cp":
        # 个人信息发送
        sql = "select account from user where name = %s"
        r = db.all(sql,[dataobj['to']])
        if len(r) == 0:#判断是否注册
            s.send(b"NR")
            return
        account = r[0][0]#目标的账号
        sql = "select * from friend where account = %s and f_account = %s"
        r = db.all(sql, [dataobj['account'],account])
        if len(r) == 0:#判断是否为好友
            s.send(b"NF")
            return
        else:
            for i in connLst:
                if i.account == account:#判断是否在线
                    dataobj['froms'] = name
                    dataobj['friendAccount'] = account
                    data = json.dumps(dataobj)+'$'
                    i.conObj.sendall(data.encode())
                    break
            else:
                print(dataobj)
                sql = "select account from user where name = %s"
                r = db.all(sql,[dataobj['to']])
                print(type(r[0][0]))
                print(r[0][0])
                print('./qqFile/' + dataobj['account'] + "_" + r[0][0] + '.txt')
                print('./qqFile/' + r[0][0] + "_" + dataobj['account'] + '.txt')
                with open('../qq/qqFile/' + dataobj['account'] + "_" + r[0][0] + '.txt', 'ab') as f:
                    print(1)
                    if "img" in dataobj['msg']:
                        f.write(("<p>" + dataobj['msg'] + "</p>").encode())
                    else:
                        f.write((dataobj['msg']).encode())
                with open('../qq/qqFile/' + r[0][0] + "_" + dataobj['account'] + '.txt', 'ab') as f1:
                    print(2)
                    if "img" in dataobj['msg']:
                        f1.write(("<p>" + dataobj['msg'] + "</p>").encode())
                    else:
                        f1.write((dataobj['msg']).encode())
                # try:
                #
                #     # f = open("./qqFile/111_132.txt", 'ab')
                #     print(1)
                #
                #     # f1 = open("./qqFile/132_111.txt", 'ab')
                #
                #     # f = open("./qqFile/" + dataobj['account'] + "_" + r[0][0] + ".txt", 'ab')
                #
                #     # f1 = open("./qqFile/" + r[0][0] + "_" + dataobj['account'] + ".txt", 'ab')
                #
                # except IOError as e:
                #     print(e)
                #     print('打开文件失败')
                # else:
                #     if "img" in dataobj['msg']:
                #         f.write(("<p>" + dataobj['msg'] + "</p>").encode())
                #         f1.write(("<p>" + dataobj['msg'] + "</p>").encode())
                #     else:
                #         f.write((dataobj['msg']).encode())
                #         f1.write((dataobj['msg']).encode())
                #     f.close()
                #     f1.close()



def do_group(s,dataobj,addr):
    if dataobj['type'] == 'ag':#创建群
        # 如果判断用户操作请求类型为添加群组则进行以下操作
        sql = "select * from groupMember where groupName = %s"
        r = db.all(sql, [dataobj['groupName']])
        if len(r) != 0:
            s.send(b'ag1')
            return
        else:
            img = str(randint(0, 26)) + ".jpg"
            sql = "insert into groupMember (groupName,member,img) values(%s,%s,%s)"
            try:
                db.zhixing(sql, [dataobj['groupName'],dataobj['account'],img])
                s.send(b'OK')
            except:
                db.rollback()
                s.send(b'ag1')

    elif dataobj['type'] == 'eg':#加入群
        groupName = dataobj['groupName']
        sql = "select * from groupMember where groupName = %s and member = %s"
        r = db.all(sql, [groupName, dataobj['account']])#是否已经加入
        if len(r) != 0:
            s.send(b'eg1')
            return
        else:
            sql = "select distinct./(img) from groupMember where groupName = %s"
            r = db.all(sql,[groupName])
            img = r[0][0]
            sql = "insert into groupMember (groupName,member,img) values(%s,%s,%s)"
            try:
                db.zhixing(sql, [groupName, dataobj['account'],img])
                s.send(b'OK')
            except:
                db.rollback()
                s.send(b'eg1')


def do_change_passwd(s,dataobj):
    sql = "select passwd from user where account = %s"
    r = db.all(sql, [dataobj['account']])
    if len(r) == 0:
        s.send(b"NI")
    elif r[0][0] == dataobj['passwd'] and len(r)>0:
        sql = "update user set passwd = %s where account = %s"
        try:
            db.zhixing(sql, [dataobj['newpasswd'],dataobj['account']])
            s.send(b'OK')
        except:
            db.rollback()
            s.send(b'FALL')
    else:
        s.send(b'NP')


def Login(account):#判断在线状态
    for i in connLst:
        if i.account == account:
            return True#在线
    return False


def do_get_msg(s,data):#获取好友列表
    account = data.split(' ')[1]
    sql = "select user.account,name,img from user,friend where f_account = user.account and friend.account = %s"
    r = db.all(sql, [account])#获取好友信息
    if len(r) == 0:
        s.send(b'N')
        return
    msg = ""
    for obj in r:
        flag = '0'#不在线
        if Login(obj[0]):
            flag = '1'
        friend = {'account':obj[0],'name':obj[1],'img':obj[2],'flag':flag}
        msg += json.dumps(friend)+'#'
    s.sendall(msg.encode())


def do_Group(s,data):#获取群信息
    account = data.split(' ')[1]
    sql = "select groupName,img from groupMember where member = %s;"
    r = db.all(sql,[account])

    if len(r) == 0:
        s.send(b'N')
        return
    msg = ""
    for obj in r:
        group = {'groupName': obj[0], 'img': obj[1]}
        msg += json.dumps(group) + '#'
    s.sendall(msg.encode())


def do_myself(s,data):
    dataList = data.split(' ')
    account = dataList[1]
    sql = "select name,img from user where account = %s;"
    r = db.all(sql,[account])
    if len(r) == 0:
        s.send(b'N')
        return
    msg = r[0][0]+' '+r[0][1]
    s.send(msg.encode())


def do_child(s,addr):
    #循环接收请求
    while True:
        data = s.recv(4096).decode("utf8","ignore")
        if not data:
            s.close()
            break

        if data == 'QT':#退出QThread线程
            s.send(b'QT')
            continue

        if data in "qQ":#退出主程序
            s.send(b'q')
            continue

        if data[0] == '{':
            dataobj = json.loads(data)
            if dataobj['type'] == "np":
                do_change_passwd(s,dataobj)
                continue

            elif dataobj['type'] in "egag":
                do_group(s,dataobj,addr)
                continue

            elif dataobj['type'] == "S":#文件发送
                send_file(s,data)
                continue

            if len(connLst) >= 1:
                do_chat(s,dataobj,data)
                continue
            # else:
            #     print(1)
                # s.sendall('-1'.encode('utf-8'))
                # continue
        else:
            if (not data) or data[0] == 'E':
                if data[0] == 'E':#退出就从在线列表中删除
                    for i in connLst:
                        if i.conObj == s:
                            connLst.remove(i)
                            break
                    s.close()
                    break
            elif data[0] == 'R':#注册
                do_register(s,data)
            elif data[0] == 'L':#登录
                do_login(s,data,addr)
            elif data[0] == 'F':#添加好友
                do_friend(s,data)
            elif data[0] == 'D':#删除好友
                do_del_friend(s,data)
            elif data[0] == 'Y':  # 获取自己信息
                do_myself(s, data)
                continue
            elif data[0] == 'M':  # 获取好友信息信号
                do_get_msg(s, data)
                continue
            elif data[0] == 'P':  # 绑定手机号
                add_phone(s, data)
                continue
            elif data[0] == 'W':  # 忘记密码
                do_forget(s, data)
                continue
            elif data[0] == 'U':  # 更改手机号
                update_phone(s, data)
                continue
            elif data[0] == 'G':  # 获取群信息
                do_Group(s, data)
                continue



class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("got connection from", self.client_address)
        s = self.request
        addr = self.client_address
        do_child(s,addr)


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',5111), MyServer)
    print('waiting for connection...')
    server.serve_forever()