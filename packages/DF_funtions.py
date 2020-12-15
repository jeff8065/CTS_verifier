#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import subprocess,os,datetime,time,openpyxl,zipfile
from packaging import version

#import version

def test(self):
	self.getselectserialID()
	print self.serialID


def defaultSettings(self):
	self.getselectserialID()
	packages  = self.packages
	features =  self.features
	propertys =  self.propertys
	print  self.androidVersion

	print "\n"+"===================== Default Settings 202005 ====================="+"\n"

	def comment(test_item,test_type,test_detail):
		check_list=[]
		if test_type is 'property' :
			for item in propertys.keys():
				if test_detail in item:
					check_list.append(item)
			if check_list:
				print test_item+":"	
				for item in check_list:
					print propertys[item]

		elif test_type is 'features':
			for x in features:
				if test_detail in x:
					check_list.append(x)
			if check_list:
				print test_item+":"
				for item in check_list:
					print item

		elif test_type is 'packages':
			for x in packages:
				if test_detail in x:
					check_list.append(x)
			if check_list:
				print test_item+":"
				for item in check_list:
					print item

		elif test_type is 'special':
			try:
				output = subprocess.check_output("adb -s "+self.serialID+" shell "+test_detail, shell=True)
				if output == "\n":
					pass
				else:
					print test_item+":"
					print output[:-1]
			except:
				pass
		elif test_type is 'meminfo':
			try:
				output = subprocess.check_output("adb -s "+self.serialID+" shell "+test_detail, shell=True)
				if output == "\n":
					pass
				else:
					#print test_item+" "
					print output[:-1]
			except:
				pass
			###############

	def check_fingerprint():
		fp_brand = propertys['ro.build.fingerprint'].split("/")[0]
		fp_name = propertys['ro.build.fingerprint'].split("/")[1]
		fp_device = propertys['ro.build.fingerprint'].split("/")[2].split(":")[0]
		for item in propertys['ro.build.fingerprint'].split("/"):
			if ":" in item:
				fp_incremental=item.split(":")[0]

		if propertys['ro.product.brand'] != fp_brand or propertys['ro.product.name'] != fp_name or propertys['ro.product.device'] != fp_device or propertys['ro.build.version.incremental'] != fp_incremental :
			print "fingerprint check:"
		if propertys['ro.product.brand'] != fp_brand :
			print('\x1b[2;32;41m' + 'ro.product.brand fail !!!' + '\x1b[0m')
		if propertys['ro.product.name'] != fp_name :
			print('\x1b[2;32;41m' + 'ro.product.name fail !!!' + '\x1b[0m')
		if propertys['ro.product.device'] != fp_device :
			print('\x1b[2;32;41m' + 'ro.product.device fail !!!' + '\x1b[0m')
		if propertys['ro.build.version.incremental'] != fp_incremental :
			print('\x1b[2;32;41m' + 'incremental fail !!!' + '\x1b[0m')
		
	################

	####################
	def EEA_check():
		print "EEA_check: "

		if 'com.google.android.feature.EEA_DEVICE'   in features  or 'com.google.android.feature.EEA_V2_DEVICE' in features:

			go_device = propertys.get('ro.config.low_ram','')
			
			## if no express_plus,install cortana
			if 'com.google.android.feature.GMSEXPRESS_PLUS_BUILD'  in features :
				print ('\x1b[2;32;41m' + "plesase check Assistant app(cortana)"+ '\x1b[0m')
				os.system(str("adb -s "+self.serialID+" install -r /CTS_tool/CTSV/cortana.apk"))
						
			if (('com.google.android.apps.searchlite'not in packages or 'com.google.android.googlequicksearchbox'not in packages) and
				'com.android.chrome' not in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print "this is type 1"
			elif (('com.google.android.apps.searchlite'not in packages or 'com.google.android.googlequicksearchbox'not in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print "this is type 2"
			elif (('com.google.android.apps.searchlite' in packages  or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome' not in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print "this is type 3a"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome' not in packages and
				'com.google.android.paid.search'  in features and
				'com.google.android.paid.chrome' not in features):
				print "this is type 3b"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print "this is type 4a"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search' in features and
				'com.google.android.paid.chrome' not in features):
				print "this is type 4b"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search'  in features and
				'com.google.android.paid.chrome'  in features):
				print "this is type 4c"
			else:
				print "wrong type"


			print "assistant check:" 			
			if ('com.google.android.googlequicksearchbox' not in packages and 'com.google.android.apps.searchlite' not in packages ):
				if go_device == "true" or go_device == "TRUE":
					if 'com.google.android.apps.actionsservice' in packages:
						print "ok"
					else:
						print ('\x1b[2;32;41m' + "go device ,this device no assistant but lack com.google.android.apps.actionsservice app"+ '\x1b[0m')
				elif go_device == "" or go_device == "false":
					if ( 'com.google.android.apps.speechservices' in packages and 'com.google.android.apps.actionsservice' in packages):
						print "ok"
					else:
						print ('\x1b[2;32;41m' + "normal device , this device no assistant but lack com.google.android.apps.speechservices or com.google.android.apps.actionsservice app"+ '\x1b[0m')
				else:
					print ('\x1b[2;32;41m' + "something wrong"+ '\x1b[0m')
			else:
				if go_device == "true"  or go_device == "TRUE":
					if 'com.google.android.apps.actionsservice' not in packages:
						print "ok"
					else:
						print ('\x1b[2;32;41m' + "go device include assistant ,can't use com.google.android.apps.actionsservice app"+ '\x1b[0m')
				elif go_device == "" or go_device == "false" :
					if ( 'com.google.android.apps.speechservices' not in packages and 'com.google.android.apps.actionsservice' not in packages):
						print "ok"
					else:
						print ('\x1b[2;32;41m' + "normal device include assistant ,can't use com.google.android.apps.speechservices or com.google.android.apps.actionsservice app"+ '\x1b[0m')
				else:
					print ('\x1b[2;32;41m' + "something wrong"+ '\x1b[0m')
		else:										
			print "none EEA"		
	###############


	########## gms core check ###########
	def gms_core_check():
		print "GMSCORE_check:"
		try:
			gmscoreversion=subprocess.check_output(str("adb -s "+ self.serialID +" shell pm dump  com.google.android.gms | grep 'versionCode'  | sed 's/versionCode=//' ").split()).splitlines()
		except:
			gmscoreversion=None
		for item in gmscoreversion:
			if int(item.split()[0][0:5])<17400:
				print ('\x1b[2;32;41m' + "gmscore version is "+item+ '\x1b[0m')
				print ('\x1b[2;32;41m' + "gmscore is lower than 17.4"+ '\x1b[0m')
	######## wellbeing priv-app check and gms check########### 
	def wellbeing_check():
		print "wellbeing_check:"
		try:
			if int(propertys.get('ro.product.first_api_level')) >= 28 :

				if "com.google.android.feature.WELLBEING" not in features:
					print ('\x1b[2;32;41m' + "no wellbeing feature "+ '\x1b[0m')

				if "com.google.android.apps.wellbeing" not in packages:
					print ('\x1b[2;32;41m' + "no wellbeing app "+ '\x1b[0m')

				try:
					gmscoreversion=subprocess.check_output(str("adb -s "+self.serialID+" shell pm dump  com.google.android.gms | grep 'versionCode'  | sed 's/versionCode=//' ").split()).splitlines()
					wellbeing_priv=subprocess.check_output(str("adb -s "+self.serialID+" shell pm dump com.google.android.apps.wellbeing | grep 'resourcePath'").split())

				except:
					wellbeing_priv=None

				if wellbeing_priv is None:
					print ('\x1b[2;32;41m' + "no wellbeing app "+ '\x1b[0m')
				else:
					if 'priv-app' not in wellbeing_priv:
						print ('\x1b[2;32;41m' + "wellbeing is not priv-app"+ '\x1b[0m')

					elif 'priv-app' in wellbeing_priv:
						print "wellbeing is priv-app"
						for item in gmscoreversion:
							if item.split()[0][0:5] <17785:
								print ('\x1b[2;32;41m' + "gmscore version is "+item+ '\x1b[0m')
								print ('\x1b[2;32;41m' + "this device have wellbeing but gmscore lower than 17.7.85"+ '\x1b[0m')
		except:
			pass

	####################




	comment("FingerPrint",'property','ro.build.fingerprint')
	comment("ClientId",'property','ro.com.google.clientidbase')
	comment("GMSPACKAGE",'property','ro.com.google.gmsversion')
	comment("Security_Patch",'property','ro.build.version.security_patch')
	comment("Manufacturer",'property','ro.product.manufacturer')
	comment("Model",'property','ro.product.model')
	comment("Low_Ram",'property','ro.config.low_ram')
	comment("MTK_swap",'property','ro.mtk_2sdcard_swap')
	comment("Platform",'property','ro.board.platform')
	comment("base_os",'property','ro.build.version.base_os')

	comment("Notch camera",'features','notch')
	comment("Cpuinfo",'special','cat proc/cpuinfo | grep "Hardware"')
	comment("Managed_users",'features','android.software.managed_users')
	comment("Device_admin",'features','android.software.device_admin')
	comment("Mtklogger",'packages','com.mediatek.mtklogger')
	comment("Fota",'packages','com.adups.fota')
	comment("Callassistant",'packages','com.android.tools.callassistant')
	comment("Telephony",'features','android.hardware.telephony')
	comment("Tachyon",'features','tachyon')
	comment("EEA_feature",'features','com.google.android.feature.EEA')
	comment("Express",'features','com.google.android.feature.GMSEXPRESS_BUILD')
	comment("Express_plus",'features','com.google.android.feature.GMSEXPRESS_PLUS_BUILD')
	comment("CleanUX",'features','CLEANUX_BUILD')
	comment("Ru_feature",'features','com.google.android.feature.RU')
	comment("TR_feature",'features','com.google.android.feature.TR_DEVICE')
	comment("TR_feature",'features','com.google.android.paid.qsb_widget')
	comment("TR_feature",'features','com.google.android.feature.TR_3P_WEBVIEW')
	comment("first_api_level",'property','ro.product.first_api_level')
	comment(' ','meminfo','cat /proc/meminfo | grep MemTotal')

	check_fingerprint()
	
	gms_core_check()
	wellbeing_check()
	
	print ""
	print "Default:Pass"
	print "Device:"	
	print "==================================================================="

	#run go fuding
	try:
		try:
			check_go = subprocess.check_output(str("adb shell getprop ro.com.google.gmsversion"), shell=True)[:-1]
			check_funding = subprocess.check_output(str('adb shell pm list features | grep -c "com.google.android.feature.GMSEXPRESS_PLUS_BUILD"'), shell=True)[:-1]
		except:
			pass
		if 'go' in check_go or 'GO' in check_go:
			str_comment='/CTS_tool/CTSV/android_go/go_check_script.sh'
			os.system(str_comment)
		
		if check_funding > 0 :
			str_comment='/CTS_tool/CTSV/GMS_ExpressPlus_test_script/Express_20200116.sh'
			os.system(str_comment)
	except:
		pass
	EEA_check()
	print "============================================================"
	print ""
	print "Please check broser intent is correct"
	print ""
	os.system(str("adb -s "+self.serialID+"  shell am start -a android.intent.action.VIEW -d http://google.com"))
	print ""
	print "===========================DF End============================="

def openFolder(self):
	os.system("nautilus "+ self.config['path']['source'])

def screenShot(self):
	self.getselectserialID()
	print "\n"+"============================screenshot============================"+"\n"
	time_Taiwan = (datetime.datetime.now()+datetime.timedelta(hours=15)).strftime("%Y%m%d")
	hostName = os.popen("whoami").readline().replace("\n","")
	#productName = subprocess.check_output(str("adb -s "+serialID+" shell getprop ro.product.model").split()).replace("\r\n","").strip().replace(" ","")
	productName = self.propertys['ro.product.model'].replace("\r\n","").strip().replace(" ","")
	folderPath = "/home/"+hostName+"/Desktop/reports/"+time_Taiwan+"/"+productName
	ticks=str(time.time())[0:10]

	if not os.path.exists(folderPath):
		os.makedirs(folderPath)

	os.system(str("adb -s "+self.serialID+" shell screencap -p /sdcard/"+ticks+".png"))
	os.system(str("adb -s "+self.serialID+" pull /sdcard/"+ticks+".png /home/"+hostName+"/Desktop/reports/"+time_Taiwan+"/"+productName+"/"))

	print "==================================================================="	

def checkfingerprint(self):
	self.getselectserialID()
	print "\n"+"==========================Fingerprint==========================="+"\n"
	print self.propertys['ro.build.fingerprint']
	print "\n"+"================================================================"+"\n"


def install_apps(self):
	self.getselectserialID()
	print "\n"+"===========================20 apps==========================="+"\n"
	if self.androidVersion is '8.0' or self.androidVersion is '7.1':
		target=21
	else:
		target=8
	for x in range(1,target):
			os.system(str("adb -s "+self.serialID+" install -r /CTS_tool/CTSV/default/test"+str(x)+".apk"))
	for y in range(1,target):
			time.sleep(1)
			os.system(str("adb -s "+self.serialID+"  shell am start -n com.example.pega3.test"+str(y)+"/.Test"+str(y)))
	print "==================================================================="	


def uninstall_apps(self):
	self.getselectserialID()
	print "=========================uninstall 20apps========================="+"\n"
	if self.androidVersion is '8.0' or self.androidVersion is '7.1':
		target=21
	else:
		target=8
	for x in range(1,target):
			os.system(str("adb -s "+self.serialID+" uninstall com.example.pega3.test"+str(x)))	
	print "\n"+"===========================End==========================="+"\n"


def xlsx(self):
	self.getselectserialID()
	print "\n"+"===========================xlsx==========================="+"\n"

	model = self.propertys['ro.product.model']
	fingerprint  = self.propertys['ro.build.fingerprint']
	clientID = self.propertys['ro.com.google.clientidbase']
	time_Taiwan = (datetime.datetime.now()+datetime.timedelta(hours=15)).strftime("%Y%m%d")
	hostName = os.popen("whoami").readline().replace("\n","")

	data_excel = openpyxl.load_workbook("/CTS_tool/CTSV/device_check_list_gms4.7.xlsx", read_only=False, keep_vba=True)

	table = data_excel.get_sheet_by_name('Cover')
	table['C25'].value = fingerprint
	table['C26'].value = clientID

	filename1 = '/home/'+hostName+'/Desktop/'+model+'_'+time_Taiwan+'_check_list_gms4.7.xlsx'
	#data_excel.save(filename=model+time_Taiwan+'_check_list_gms4.6.xlsx')
	data_excel.save(filename1)

	print "==================================================================="	


def installVerifier (self):
	print "\n=========================Install Verifier==========================\n"
	self.getselectserialID()
	sourse=self.config['path']['source']+self.androidVersion+"/android-cts-verifier-"+self.androidVersion+"_r"+self.config['version']["cts"+str(eval(self.androidVersion))]+"-linux_x86-"+self.deviceType+".zip"

	if os.path.exists(str(self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType)):
		pass
	else:
		if os.path.exists(sourse):
			print "zip file exists, unzip now......\n"
			# sourse=config['path']['source']+androidVersion+"/android-cts-verifier-"+androidVersion+"_r"+config['version']["cts"+str(eval(androidVersion))]+"-linux_x86-"+deviceType+".zip"
			extract_to=self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType
			unzip=zipfile.ZipFile(sourse)
			unzip.extractall(extract_to)
			unzip.close
		else:
			print "verifier zip is not exists"
			print "please download from 'https://source.android.com/compatibility/cts/downloads'"
		
	if version.parse(self.androidVersion) >= version.parse("4.4"):
		os.system(self.install_cmd+"CtsVerifier.apk")

	if version.parse(self.androidVersion) >= version.parse("5.0"):
		os.system(self.install_cmd+"NotificationBot.apk")

	if version.parse(self.androidVersion) >= version.parse("8.0"):
		os.system(self.push_cmd+"NotificationBot.apk  /sdcard/")
		os.system(self.install_cmd+"CtsEmptyDeviceAdmin.apk")
		os.system(self.install_cmd+"CtsVerifierUSBCompanion.apk")
		os.system(self.install_cmd+"CtsVpnFirewallAppApi23.apk")
		if self.deviceType == "x86":
			print "please install openCV  by yourself"
			os.system("nautilus "+ self.config['path']['source']+"OpenCV-android-sdk")
		else:
			os.system(str("adb -s "+self.serialID+" install -r  "+self.config['path']['source']+"OpenCV-android-sdk/OpenCV_3.0.0_Manager_3.00_"+self.abiType+".apk"))

	if version.parse(self.androidVersion) >= version.parse("10"):
		os.system(self.push_cmd+"NotificationBot.apk  /data/local/tmp/")
		os.system(self.install_cmd+"CtsForceStopHelper.apk")
		os.system(str("adb -s "+self.serialID+ " install -r "+self.config['path']['source']+"MIDI_BLE.apk"))
		os.system(self.instant_cmd+"CtsVerifierInstantApp.apk")
		#for create report
		os.system("adb -s " +self.serialID+ " shell appops set com.android.cts.verifier android:read_device_identifiers allow")
		

					# if version.parse(androidVersion) >= version.parse("9.0"):
					# 	os.system(install_cmd+"NotificationBot.apk")
					# 	if version.parse(androidVersion) >= version.parse("10"):
					# 		os.system(install_cmd+"NotificationBot.apk")

	print "\n==================================================================="	


def adb39 (self):
	print "\n=========================adb 39==========================\n"
	adb_path = subprocess.check_output("adb | grep Install", shell=True).splitlines()[0].replace('Installed as ','').replace('/platform-tools/adb','')
	os.system(str("rm -r "+adb_path+"/platform-tools"))
	os.system(str("cp -rp "+self.config['path']['source']+"ADB_platform_v39/platform-tools "+adb_path+'/platform-tools'))
	os.system(str("adb kill-server ; adb version ; adb start-server"))
	print "\n==================================================================="	

def adb40 (self):
	print "\n=========================adb 40==========================\n"
	adb_path = subprocess.check_output("adb | grep Install", shell=True).splitlines()[0].replace('Installed as ','').replace('/platform-tools/adb','')
	os.system(str("rm -r "+adb_path+"/platform-tools"))
	os.system(str("cp -rp "+self.config['path']['source']+"ADB_platform_v40/platform-tools "+adb_path+'/platform-tools'))
	os.system(str("adb kill-server ; adb version ; adb start-server"))
	print "\n==================================================================="	

def adb41 (self):
	print "\n=========================adb 41==========================\n"
	adb_path = subprocess.check_output("adb | grep Install", shell=True).splitlines()[0].replace('Installed as ','').replace('/platform-tools/adb','')
	os.system(str("rm -r "+adb_path+"/platform-tools"))
	os.system(str("cp -rp "+self.config['path']['source']+"ADB_platform_v41/platform-tools "+adb_path+'/platform-tools'))
	os.system(str("adb kill-server ; adb version ; adb start-server"))
	print "\n==================================================================="	

def EEA_V2(self):
	self.getselectserialID()
	print " 請在OOBE時就登入 EEA test account"
	print " 選擇google作為預設Search engine"
	print " 打開USB debug後 >> 跑腳本"

	print "Item E1"
	print  "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep  EEA  '))
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep  paid  '))
	print "-------------------------------------------------------------------------------------\n"

	print "Item E3"
	print  "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine  '))
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine_aga  '))
	print "-------------------------------------------------------------------------------------\n"

	print "Item E4"
	print  "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine  '))
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine_chrome  '))
	print "-------------------------------------------------------------------------------------\n"


def Turkey(self):
	self.getselectserialID()

	print "Item T1"
	print  "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep TR  '))
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep paid  '))
	print "-------------------------------------------------------------------------------------\n"

	print "Item T3"
	print  "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell content query --uri content://com.google.settings/partner | grep "client_id"  '))
	print "-------------------------------------------------------------------------------------\n"



if __name__ == '__main__':
	os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
	
