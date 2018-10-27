# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import http.client
import urllib
import json
import string
import random

host = "api.voice.ihuyi.com"
sms_send_uri = "/webservice/voice.php?method=Submit"

# APIID
account = 'V67043084'

password = '07ff6c2be9b657fa60ebbeea4c1117b9'
# account = 'V78517404'
# password = '3d357cd2deb3314883c7785138bc2b36'



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
    code = ''.join(str(i) for i in random.sample(range(1, 10), 4))
    mobile = str(mobile)
    text = str(code)
    send_sms(text,mobile)
    return code
