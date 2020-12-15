#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import subprocess, os , time
import DF_funtions

def property_check(self):
	pass

def Exo_app(self):
	pass

def install_apks(self):
	pass

def test(self):
	self.getselectserialID()
	os.system("adb -s "+self.serialID+" shell am start -a android.intent.action.VIEW 'http://www.youtube.com/watch?v=yUomplw4lQ0'")
	time.sleep( 5 )
	DF_funtions.screenShot(self)




if __name__ == '__main__':
	os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
	