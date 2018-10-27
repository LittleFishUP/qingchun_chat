#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import http.client
import urllib
import json
import string
import random
host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# APIID APIKEY
account = "C15787314"
password = "a3e87b4329937aa9f3bb1742a3e4f305"



def send_sms(text, mobile):
    params = urllib.parse.urlencode({'account': account, 'password': password,
                                     'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def dxyz(mobile):
    code = ''.join(str(i) for i in random.sample(range(1, 10), 6))
    mobile = str(mobile)
    text = "您的验证码是：{}。请不要把验证码泄露给其他人。".format(code)
    send_sms(text, mobile)
    return code #验证码
