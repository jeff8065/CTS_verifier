#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import subprocess, os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def up(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 19")
def left(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 21")
def right(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 22")
def down(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 20")
def enter(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 66")
def back(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 04")
def home(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 03")  
def recent(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent KEYCODE_APP_SWITCH")    

def camera(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 27")   
def mute(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent 164")    

def text(self):
	self.getselectserialID()
	print self.entryText.get()
	os.system("adb -s "+self.serialID+' shell input text  "'+ self.entryText.get()+'"' )    

def presstext(self):
	self.getselectserialID()
	print  "search \""+self.pressText.get()+ "\" and press it"
	def get_all_item(serialID):
		def output(serialID):
			while True:
				output=subprocess.check_output("adb -s "+serialID+" exec-out uiautomator dump /dev/tty", shell=True)
				if "ERROR: null root node returned by UiTestAutomationBridge" in output:
					time.sleep(1)
				else:
					return output.replace("UI hierchary dumped to: /dev/tty","")

		tree = ET.ElementTree(ET.fromstring(output(serialID)))
		item=[]

		def get_bound(string):
			return string.replace("[", "").replace("]", " ").replace(",", " ").split(" ")

		for elem in tree.iter():
			dic = {}
			try:
				if elem.attrib['text'] != "":
					dic['text']=elem.attrib['text']
				elif elem.attrib['resource-id'] == 'com.android.cts.verifier:id/pass_button':
					dic['text']='Pass_icon'
				if dic['text'] != "":
					x = (int(get_bound(elem.attrib['bounds'])[0]) + int(get_bound(elem.attrib['bounds'])[2])) / 2
					y = (int(get_bound(elem.attrib['bounds'])[1]) + int(get_bound(elem.attrib['bounds'])[3])) / 2
					dic['bounds']= str(x) + " " + str(y)
					item.append(dic)
			except:
				pass
		# item
		# [ {'text': 'Camera Flashlight', 'bounds': '188 90'}, {'text': 'Press Start to start flashlight test.', 'bounds': '360 667'} ]
		return item
	def tap(serialID,target, loop):
		item = get_all_item(serialID)
		for x in range(len(item)):
			if item[x]['text']==target:
				bounds=item[x]['bounds']
		if loop == "1":
			cmd = 'gnome-terminal --  /bin/sh -c ' + "\'watch -n 5 adb -s "+serialID+ " shell input tap "+ bounds+"; exec bash\'"
			#gnome-terminal -- /bin/sh -c 'watch -n 3 adb devices; exec bash'
			os.system(cmd)    
		else:
			subprocess.call("adb -s " + serialID + " shell input tap "+ bounds, shell=True)
			#gnome-terminal -e 'sh -c "adb devices; exec bash"'
	tap(self.serialID , self.pressText.get(),self.loopValue.get())


def opensetting(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+ " shell am start -a android.settings.SETTINGS")

def kill_recent(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell input keyevent KEYCODE_APP_SWITCH")    
	os.system("adb -s "+self.serialID+" shell input keyevent DEL")    


def  stayawake(self):
    self.getselectserialID()
    os.system("adb -s "+self.serialID+" shell settings put global stay_on_while_plugged_in 0")
    os.system("adb -s "+self.serialID+" shell settings put system accelerometer_rotation 0")
	
if __name__ == '__main__':
	os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
	