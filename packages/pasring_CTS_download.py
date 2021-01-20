#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests,os,subprocess
from bs4 import BeautifulSoup
#from lxml import html
#res = requests.get('https://3pl.pegatroncorp.com')
#print(res.text)
#from urllib.request import urlopen
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import re
import requests
from bs4 import BeautifulSoup


def download(self):


    r = requests.get("https://source.android.com/compatibility/cts/downloads") #將此頁面的HTML GET下來
    #print(r.text) #印出HTML
    #網頁資料GET下來
    soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
    sel =soup.find_all('a', {'href':re.compile("https://dl.google.com/dl/android/cts/android-cts-verifier-")}) #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    for s in sel:
        #print(s["href"], s.text) 
        s = str(s)
        #print (s.split("a href=\"",)[1].split("\">",)[0]) # download網址
        wdownload = str(s).split("a href=\"",)[1].split("\">",)[0] # 分割網址字串
        sname =s.split("a href=\"",)[1].split("\">",)[0].split("/cts/",)[1] #檔案名稱
       # print (sname.split("verifier-",)[1].split("_",)[0])
        version=(sname.split("verifier-",)[1].split("_",)[0])
        ww=subprocess.check_output(str("find /CTS_tool/CTSV/ -name "+ str(sname)).split())
        ww =str(ww).strip("b").strip("'").replace("\r\n","")
        #print (ww)
        if ww == "":
        	print ("未下載")  
        	print (sname)
        	os.system("wget "+ str(wdownload)+" -P /CTS_tool/CTSV/" + version +"/") #下載檔案
        else:
        	print("目前最新" +sname )

if __name__ == '__main__':
    os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
    
