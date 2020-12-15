#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import subprocess, os, datetime
from packaging import version

def ITS(self):
	pass


def USB_Debugging(self):
	self.getselectserialID()
	print "\n"+"============================= USB_Debugging =============================="+"\n"
	os.system("adb -s "+self.serialID+" shell am start -e fingerprints placeholder -e key placeholder -e key placeholder com.android.systemui/.UsbDebuggingActivityAlias")
	print "\n"+"==================================================================="	

def remove_admin(self):
	self.getselectserialID()
	print "\n"+"============================= remove admin =============================="+"\n"
	os.system("adb -s "+self.serialID+" shell dpm remove-active-admin com.android.cts.emptydeviceowner/.EmptyDeviceAdmin")
	print "\n"+"==================================================================="	


def UID(self):
	self.getselectserialID()
	print "\n"+"============================= set UID =============================="+"\n"
	os.system("adb -s "+self.serialID+" shell cmd sensorservice set-uid-state com.android.cts.verifier idle")
	print "\n"+"==================================================================="	



def UID2(self):
	self.getselectserialID()
	print "\n"+"============================= reset UID =============================="+"\n"
	os.system("adb -s "+self.serialID+" shell cmd sensorservice reset-uid-state com.android.cts.verifier")
	print "\n"+"==================================================================="	



def BYOD_VPN_23(self):
	self.getselectserialID()
	print "\n"+"============================= install VPN23 =============================="+"\n"
	os.system(self.uninstall_cmd+"  com.android.cts.vpnfirewall")
	os.system(self.install_cmd+"CtsVpnFirewallAppApi23.apk")
	print "\n"+"==================================================================="	


def BYOD_VPN_24(self):
	self.getselectserialID()
	print "\n"+"============================= install VPN24 =============================="+"\n"
	os.system(self.uninstall_cmd+" uninstall com.android.cts.vpnfirewall")
	os.system(self.install_cmd+"CtsVpnFirewallAppApi24.apk")
	print "\n"+"==================================================================="	


def BYOD_VPN_NAO(self):
	self.getselectserialID()
	print "\n"+"============================= install  NotAlwaysOn =============================="+"\n"
	os.system(self.uninstall_cmd+" uninstall com.android.cts.vpnfirewall")
	os.system(self.install_cmd+"CtsVpnFirewallAppNotAlwaysOn.apk")
	print "\n"+"==================================================================="	



def newOwner(self):
	self.getselectserialID()
	print "\n"+"============================= android O device-owner =============================="+"\n"
	os.system(self.install_t_cmd+"CtsEmptyDeviceOwner.apk")
	os.system(str("adb -s "+ self.serialID +" shell dpm set-device-owner com.android.cts.emptydeviceowner/.EmptyDeviceAdmin"))
	print "\n"+"==================================================================="	


def deviceOwner(self):
	self.getselectserialID()
	print "\n"+"=========================== device-owner ==========================="+"\n"
	os.system(str("adb -s "+self.serialID+" shell dpm set-device-owner 'com.android.cts.verifier/com.android.cts.verifier.managedprovisioning.DeviceAdminTestReceiver'"))
	print "==================================================================="	

def bmgr_run(self):
	self.getselectserialID()
	print "\n"+"============================= bmgr run =============================="+"\n"
	os.system(str("adb -s "+self.serialID+" shell bmgr run"))
	print "adb shell bmgr run"
	os.system(str("adb -s "+self . serialID+" shell bmgr run"))
	print "adb shell bmgr run"
	os.system(str("adb -s "+self.serialID+" shell bmgr run"))
	print "adb shell bmgr run"
	print "\n"+"==================================================================="	


def Perimission(self):
	self.getselectserialID()
	print "\n"+"============================= install Perimission =============================="+"\n"
	os.system(self.install_cmd+"CtsPermissionApp.apk")
	print "\n"+"==================================================================="	

def CompassButton(self):
	self.getselectserialID()
	print "\n"+"============================= install Perimission =============================="+"\n"
	os.system(str("adb -s "+self.serialID+ " install -r "+self.config['path']['source']+"360Viewer.apk"))
	os.system(str("adb -s "+self.serialID+ " install -r "+self.config['path']['source']+"Compass.apk"))

	print "\n"+"==================================================================="	


def Pull(self):
	self.getselectserialID()
	print "\n"+"============================= Pull report =============================="+"\n"
	time_Taiwan = (datetime.datetime.now()+datetime.timedelta(hours=15)).strftime("%Y%m%d")
	hostName = os.popen("whoami").readline().replace("\n","")
	#productName = subprocess.check_output(str("adb -s "+serialID+" shell getprop ro.product.model").split()).replace("\r\n","").strip().replace(" ","")
	productName = self.propertys['ro.product.model'].replace("\r\n","").strip().replace(" ","")
	folderPath = "/home/"+hostName+"/Desktop/reports/"+time_Taiwan+"/"+productName
	
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)

	if version.parse(self.androidVersion) >= version.parse("10"):
		os.system("adb -s " +self.serialID+ " shell appops set com.android.cts.verifier android:read_device_identifiers allow")
	#Note: Use adb shell am get-current-user to get the CURRENT_USER ID.
	# adb shell content query --user CURRENT_USER --uri   content://com.android.cts.verifier.testresultsprovider/reports/latest > report.zip
	
	
	if version.parse(self.androidVersion) >= version.parse("9"):
		os.system(str("adb -s "+self.serialID+" pull /sdcard/verifierReports "+  "/home/"+hostName+"/Desktop/reports/"+time_Taiwan+"/"+productName))
	elif  version.parse(self.androidVersion) >= version.parse("7"):
		os.system(str("adb -s "+self.serialID+" pull /storage/emulated/0/verifierReports "+  "/home/"+hostName+"/Desktop/reports/"+time_Taiwan+"/"+productName))
	else:
		os.system(str("adb -s "+self.serialID+" pull /sdcard/ctsVerifierReports "+  "/home/"+hostName+"/Desktop/reports/"+time_Taiwan+"/"+productName))

	print "==================================================================="			

	
if __name__ == '__main__':
	os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
	
