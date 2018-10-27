from pymysql import *

class Mysqlpython:
    def __init__(self,database,
                 host="localhost",
                 user="root",
                 password="123456",
                 port=3306,
                 charset="utf8"):
        self.host = host
        self.user =user
        self.password = password
        self.port = port
        self.charset = charset
        self.database = database

    def open(self):
        self.db = connect(host=self.host,
                          user=self.user,
                          port=self.port,
                          database=self.database,
                          password=self.password,
                          charset=self.charset)
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def zhixing(self,sql,L=[]):    # pymysql.execute(sql)
        try:
            self.open()
            self.cur.execute(sql,L)
            self.db.commit()
            print("ok")
        except Exception as e:
            self.db.rollback()
            print("Failed",e)
        self.close()

    def all(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print("Failed",e)
        self.close()

    def rollback(self):
        self.db.rollback()

