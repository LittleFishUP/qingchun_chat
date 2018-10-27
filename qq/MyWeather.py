# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtGui import QIcon 

import urllib.request
import gzip
import json

# global m4Days
m4Days=0

def get_weather_data(cityName) :
    #city_name = input('请输入要查询的城市名称：')
    url1 = 'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.parse.quote(cityName)
    #网址1只需要输入城市名，网址2需要输入城市代码
    weather_data = urllib.request.urlopen(url1).read()
    #读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    #解压网页数据
    weather_dict = json.loads(weather_data)
    #将json数据转换为dict数据
    return weather_dict

def show_weather(weather_data,m4Days):
    weather_dict = weather_data 
    #将json数据转换为dict数据
    if weather_dict.get('desc') == 'invilad-citykey':
        weather_str='你输入的城市名有误，或者天气中心未收录你所在城市'
    elif weather_dict.get('desc') =='OK':
        forecast = weather_dict.get('data').get('forecast')
        weather_str='城市：'+weather_dict.get('data').get('city')+'\n'
        weather_str=weather_str + '温度：' + weather_dict.get('data').get('wendu')+'℃ '+'\n'
        weather_str=weather_str + '感冒：' + weather_dict.get('data').get('ganmao') +'\n'
        weather_str=weather_str + '风向：'+forecast[0].get('fengxiang')+'\n'
        wind_level=forecast[0].get('fengli')
        tailor_str=wind_level[wind_level.index('[CDATA[')+7:wind_level.index(']]')]
        weather_str=weather_str + '风级：'+tailor_str+'\n'

        #weather_str=weather_str + '风级：'+forecast[0].get('fengli')+'\n'
        weather_str=weather_str + '高温：'+forecast[0].get('high')+'\n'
        weather_str=weather_str + '低温：'+forecast[0].get('low')+'\n'
        weather_str=weather_str + '天气：'+forecast[0].get('type')+'\n'
        weather_str=weather_str + '日期：'+forecast[0].get('date')+'\n'
        weather_str=weather_str + '**********************************************'+'\n'
        if m4Days==1:
            for i in range(1,5):
                weather_str=weather_str +'日期：'+forecast[i].get('date')+'\n'
                weather_str=weather_str +'风向：'+forecast[i].get('fengxiang')+'\n'
                wind_level=forecast[i].get('fengli')
                tailor_str=wind_level[wind_level.index('[CDATA[')+7:wind_level.index(']]')]
                weather_str=weather_str +'风级：'+tailor_str+'\n'
                #weather_str=weather_str +'风级：'+forecast[i].get('fengli')+'\n'
                weather_str=weather_str +'高温：'+forecast[i].get('high')+'\n'
                weather_str=weather_str +'低温：'+forecast[i].get('low')+'\n'
                weather_str=weather_str +'天气：'+forecast[i].get('type')+'\n'
                weather_str=weather_str +'--------------------------'+'\n'
    weather_str=weather_str +'**********************************************'+'\n'
    return weather_str


from ui_WeatherForecast import Ui_Form

class myWeather(QDialog, Ui_Form):
    global m4Days
    global mStr
    global mCityStr
    def __init__(self,parent=None):  
        super(myWeather,self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('MostlySunny.ico'))
        self.checkBox.stateChanged.connect(self.checkboxstate)
        self.CitypushButton01.clicked.connect(lambda: self.hotcity(1))
        self.CitypushButton02.clicked.connect(lambda: self.hotcity(2))
        self.CitypushButton03.clicked.connect(lambda: self.hotcity(3))
        self.CitypushButton04.clicked.connect(lambda: self.hotcity(4))
        self.CitypushButton05.clicked.connect(lambda: self.hotcity(5))
        self.CitypushButton06.clicked.connect(lambda: self.hotcity(6))
        self.CitypushButton07.clicked.connect(lambda: self.hotcity(7))
        self.CitypushButton08.clicked.connect(lambda: self.hotcity(8))
        self.CitypushButton09.clicked.connect(lambda: self.hotcity(9))
        self.CitypushButton10.clicked.connect(lambda: self.hotcity(10))
        self.CitypushButton11.clicked.connect(lambda: self.hotcity(11))
        self.CitypushButton12.clicked.connect(lambda: self.hotcity(12))
        self.CitypushButton13.clicked.connect(lambda: self.hotcity(13))
        self.CitypushButton14.clicked.connect(lambda: self.hotcity(14))
        self.CitypushButton15.clicked.connect(lambda: self.hotcity(15))
        self.CitypushButton16.clicked.connect(lambda: self.hotcity(16))
        self.CitypushButton17.clicked.connect(lambda: self.hotcity(17))
        self.CitypushButton18.clicked.connect(lambda: self.hotcity(18))
        self.CitypushButton19.clicked.connect(lambda: self.hotcity(19))
        self.CitypushButton20.clicked.connect(lambda: self.hotcity(20))

        self.pushButton.clicked.connect(self.checkWeather)


    def checkboxstate(self,state):
        global m4Days
        if(state==QtCore.Qt.Unchecked):
            m4Days=0
        else:
            m4Days=1
        #print ('Check Box state=', m4Days)

    def hotcity(self,n):

        if (n==1):
          cityName=self.CitypushButton01.text()
          self.lineEdit.setText(cityName)
        elif (n==2):
          cityName=self.CitypushButton02.text()
          self.lineEdit.setText(cityName)
        elif (n==3):
          cityName=self.CitypushButton03.text()
          self.lineEdit.setText(cityName)
        elif (n==4):
          cityName=self.CitypushButton04.text()
          self.lineEdit.setText(cityName)
        elif (n==5):
          cityName=self.CitypushButton05.text()
          self.lineEdit.setText(cityName)
        elif (n==6):
          cityName=self.CitypushButton06.text()
          self.lineEdit.setText(cityName)
        elif (n==7):
          cityName=self.CitypushButton07.text()
          self.lineEdit.setText(cityName)
        elif (n==8):
          cityName=self.CitypushButton08.text()
          self.lineEdit.setText(cityName)
        elif (n==9):
          cityName=self.CitypushButton09.text()
          self.lineEdit.setText(cityName)
        elif (n==10):
          cityName=self.CitypushButton10.text()
          self.lineEdit.setText(cityName)
        elif (n==11):
          cityName=self.CitypushButton11.text()
          self.lineEdit.setText(cityName)
        elif (n==12):
          cityName=self.CitypushButton12.text()
          self.lineEdit.setText(cityName)
        elif (n==13):
          cityName=self.CitypushButton13.text()
          self.lineEdit.setText(cityName)
        elif (n==14):
          cityName=self.CitypushButton14.text()
          self.lineEdit.setText(cityName)
        elif (n==15):
          cityName=self.CitypushButton15.text()
          self.lineEdit.setText(cityName)
        elif (n==16):
          cityName=self.CitypushButton16.text()
          self.lineEdit.setText(cityName)
        elif (n==17):
          cityName=self.CitypushButton17.text()
          self.lineEdit.setText(cityName)
        elif (n==18):
          cityName=self.CitypushButton18.text()
          self.lineEdit.setText(cityName)
        elif (n==19):
          cityName=self.CitypushButton19.text()
          self.lineEdit.setText(cityName)
        elif (n==20):
          cityName=self.CitypushButton20.text()
          self.lineEdit.setText(cityName)
        else:
          self.textEdit.setText('城市名称错误')


    def checkWeather(self):
        global m4Days
        cityName=self.lineEdit.text()
        mStr=show_weather(get_weather_data(cityName),m4Days)
        self.textEdit.setText(mStr)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()





# if __name__=="__main__":
#     import sys
#     global m4Days
#
#     m4Days=0
#
#     app=QApplication(sys.argv)
#     myshow=myWeather()
#     myshow.show()
#     sys.exit(app.exec_())
