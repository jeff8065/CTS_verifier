#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import subprocess,os,datetime,time,openpyxl,zipfile

import ttk
from Tkinter import *
from packaging import version

import tkMessageBox


#ss=""
#import version

def test(self):
	self.getselectserialID()
	print >> w , self.serialID


def defaultSettings(self):
	self.getselectserialID()
	packages  = self.packages
	features =  self.features
	propertys =  self.propertys

#	print >> w ,(self.androidVersion)
	devicename=subprocess.check_output(str("adb -s " + self.serialID + " shell getprop ro.build.product").split()).replace("\n","")
	w = open('/CTS_tool/CTSV/3PL_verifier/default_check/'+str(devicename)+"_"+time.strftime("%Y-%m-%d")+".txt", 'w+')
	
	print >> w , "\n"+"===================== Default Settings 202005 ====================="+"\n"

	def comment(test_item,test_type,test_detail):
		check_list=[]
		f = open('file_io.txt', 'a')
		if test_type is 'property' :
			for item in propertys.keys():
				if test_detail in item:
					check_list.append(item)

			if check_list:
				print >> w , test_item+":"	
				for item in check_list:
					
					print >> w , propertys[item]
				#	ss = propertys[item]
				#	print >> w ,(ss)
				#	list_test(str(ss))

					f.write(test_item+": "+"\n"  +propertys[item]+"\n")
					


		elif test_type is 'features':
			for x in features:
				if test_detail in x:
					check_list.append(x)
			if check_list:
				print >> w , test_item+":"
				f.write(test_item+": "+"\n")
				for item in check_list:
					print >> w , item
					f.write(item+"\n")
		elif test_type is 'packages':
			for x in packages:
				if test_detail in x:
					check_list.append(x)
			if check_list:
				print >> w , test_item+":"
				f.write(test_item+": "+"\n" )
				for item in check_list:
					print >> w , item
					f.write(item+"\n")
		elif test_type is 'special':
			f.write(test_item+": "+"\n")
			try:
				output = subprocess.check_output("adb -s "+self.serialID+" shell "+test_detail, shell=True)
				
				if output == "\n":
					pass
				else:
					print >> w , test_item+":"
					print >> w , output[:-1]
					f.write(output[:-1]+"\n")
			except:
				pass
		elif test_type is 'meminfo':
			f.write("meminfo:"+"\n")
			try:
				output = subprocess.check_output("adb -s "+self.serialID+" shell "+test_detail, shell=True)
				if output == "\n":
					pass
				else:
					#print >> w , test_item+" "
					print >> w , output[:-1]
					f.write(output[:-1]+"\n")
			except:
				pass

		f.close()

			###############

	def check_fingerprint():
		fp_brand = propertys['ro.build.fingerprint'].split("/")[0]
		fp_name = propertys['ro.build.fingerprint'].split("/")[1]
		fp_device = propertys['ro.build.fingerprint'].split("/")[2].split(":")[0]
		for item in propertys['ro.build.fingerprint'].split("/"):
			if ":" in item:
				fp_incremental=item.split(":")[0]

		if propertys['ro.product.brand'] != fp_brand or propertys['ro.product.name'] != fp_name or propertys['ro.product.device'] != fp_device or propertys['ro.build.version.incremental'] != fp_incremental :
			print >> w , "fingerprint check:"
		if propertys['ro.product.brand'] != fp_brand :
			#need color item print >> w ,('\x1b[2;32;41m' + 'ro.product.brand fail !!!' + '\x1b[0m')
			print >> w ,('ro.product.brand fail !!!')
		if propertys['ro.product.name'] != fp_name :
			#need color item print >> w ,('\x1b[2;32;41m' + 'ro.product.name fail !!!' + '\x1b[0m')
			print >> w ,('ro.product.name fail !!!')
		if propertys['ro.product.device'] != fp_device :
			#need color item  print >> w ,('\x1b[2;32;41m' + 'ro.product.device fail !!!' + '\x1b[0m')
			print >> w ,('ro.product.device fail !!!')
		if propertys['ro.build.version.incremental'] != fp_incremental :
			#need color item print >> w ,('\x1b[2;32;41m' + 'incremental fail !!!' + '\x1b[0m')
			print >> w ,('incremental fail !!!')
		
	################

	####################
	def EEA_check():
		print >> w , "EEA_check: "

		if 'com.google.android.feature.EEA_DEVICE'   in features  or 'com.google.android.feature.EEA_V2_DEVICE' in features:

			go_device = propertys.get('ro.config.low_ram','')
			
			## if no express_plus,install cortana
			if 'com.google.android.feature.GMSEXPRESS_PLUS_BUILD'  in features :
				#need color item # print >> w , ('\x1b[2;32;41m' + "plesase check Assistant app(cortana)"+ '\x1b[0m')
				print >> w , ("plesase check Assistant app(cortana)")
				os.system(str("adb -s "+self.serialID+" install -r /CTS_tool/CTSV/cortana.apk"))
						
			if (('com.google.android.apps.searchlite'not in packages or 'com.google.android.googlequicksearchbox'not in packages) and
				'com.android.chrome' not in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print >> w , "this is type 1"
			elif (('com.google.android.apps.searchlite'not in packages or 'com.google.android.googlequicksearchbox'not in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print >> w , "this is type 2"
			elif (('com.google.android.apps.searchlite' in packages  or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome' not in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print >> w , "this is type 3a"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome' not in packages and
				'com.google.android.paid.search'  in features and
				'com.google.android.paid.chrome' not in features):
				print >> w , "this is type 3b"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search' not in features and
				'com.google.android.paid.chrome' not in features):
				print >> w , "this is type 4a"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search' in features and
				'com.google.android.paid.chrome' not in features):
				print >> w , "this is type 4b"
			elif (('com.google.android.apps.searchlite' in packages or 'com.google.android.googlequicksearchbox' in packages) and
				'com.android.chrome'  in packages and
				'com.google.android.paid.search'  in features and
				'com.google.android.paid.chrome'  in features):
				print >> w , "this is type 4c"
			else:
				print >> w , "wrong type"


			print >> w , "assistant check:" 			
			if ('com.google.android.googlequicksearchbox' not in packages and 'com.google.android.apps.searchlite' not in packages ):
				if go_device == "true" or go_device == "TRUE":
					if 'com.google.android.apps.actionsservice' in packages:
						print >> w , "ok"
					else:
						print >> w , ("go device ,this device no assistant but lack com.google.android.apps.actionsservice app")

						#need color item #	print >> w , ('\x1b[2;32;41m' + "go device ,this device no assistant but lack com.google.android.apps.actionsservice app"+ '\x1b[0m')
						

				elif go_device == "" or go_device == "false":
					if ( 'com.google.android.apps.speechservices' in packages and 'com.google.android.apps.actionsservice' in packages):
						print >> w , "ok"
					else:
					#need color item #	print >> w , ('\x1b[2;32;41m' + "normal device , this device no assistant but lack com.google.android.apps.speechservices or com.google.android.apps.actionsservice app"+ '\x1b[0m')
						print >> w , ("normal device , this device no assistant but lack com.google.android.apps.speechservices or com.google.android.apps.actionsservice app")
				else:
					#need color item #print >> w , ('\x1b[2;32;41m' + "something wrong"+ '\x1b[0m')
					print >> w , ("something wrong")
			else:
				if go_device == "true"  or go_device == "TRUE":
					if 'com.google.android.apps.actionsservice' not in packages:
						print >> w , "ok"
					else:
					#need color item #	print >> w , ('\x1b[2;32;41m' + "go device include assistant ,can't use com.google.android.apps.actionsservice app"+ '\x1b[0m')
						print >> w , ("go device include assistant ,can't use com.google.android.apps.actionsservice app")
				elif go_device == "" or go_device == "false" :
					if ( 'com.google.android.apps.speechservices' not in packages and 'com.google.android.apps.actionsservice' not in packages):
						print >> w , "ok"
					else:
					#need color item #	print >> w , ('\x1b[2;32;41m' + "normal device include assistant ,can't use com.google.android.apps.speechservices or com.google.android.apps.actionsservice app"+ '\x1b[0m')
						print >> w , ("normal device include assistant ,can't use com.google.android.apps.speechservices or com.google.android.apps.actionsservice app")
				else:
					#need color item #print >> w , ('\x1b[2;32;41m' + "something wrong"+ '\x1b[0m')
					print >> w , ("something wrong")
		else:										
			print >> w , "none EEA"		
	###############


	########## gms core check ###########
	def gms_core_check():
		print >> w , "GMSCORE_check:"
		try:
			gmscoreversion=subprocess.check_output(str("adb -s "+ self.serialID +" shell pm dump  com.google.android.gms | grep 'versionCode'  | sed 's/versionCode=//' ").split()).splitlines()
		except:
			gmscoreversion=None
		for item in gmscoreversion:
			if int(item.split()[0][0:5])<17400:
				#need color item print >> w , ('\x1b[2;32;41m' + "gmscore version is "+item+ '\x1b[0m')
				#need color item print >> w , ('\x1b[2;32;41m' + "gmscore is lower than 17.4"+ '\x1b[0m')
				print >> w , ("gmscore version is "+item)
				print >> w , ("gmscore is lower than 17.4")
	######## wellbeing priv-app check and gms check########### 
	def wellbeing_check():
		print >> w , "wellbeing_check:"
		try:
			if int(propertys.get('ro.product.first_api_level')) >= 28 :

				if "com.google.android.feature.WELLBEING" not in features:
					#need color item print >> w , ('\x1b[2;32;41m' + "no wellbeing feature "+ '\x1b[0m')
					print >> w , ("no wellbeing feature ")


				if "com.google.android.apps.wellbeing" not in packages:
					#need color item print >> w , ('\x1b[2;32;41m' + "no wellbeing app "+ '\x1b[0m')
					print >> w , ( "no wellbeing app ")

				try:
					gmscoreversion=subprocess.check_output(str("adb -s "+self.serialID+" shell pm dump  com.google.android.gms | grep 'versionCode'  | sed 's/versionCode=//' ").split()).splitlines()
					wellbeing_priv=subprocess.check_output(str("adb -s "+self.serialID+" shell pm dump com.google.android.apps.wellbeing | grep 'resourcePath'").split())

				except:
					wellbeing_priv=None

				if wellbeing_priv is None:
					#need color item print >> w , ('\x1b[2;32;41m' + "no wellbeing app "+ '\x1b[0m')
					print >> w , ("no wellbeing app ")
				else:
					if 'priv-app' not in wellbeing_priv:
						#need color item print >> w , ('\x1b[2;32;41m' + "wellbeing is not priv-app"+ '\x1b[0m')
						print >> w , ("wellbeing is not priv-app")

					elif 'priv-app' in wellbeing_priv:
						print >> w , "wellbeing is priv-app"
						for item in gmscoreversion:
							if item.split()[0][0:5] <17785:
							#need color item 	print >> w , ('\x1b[2;32;41m' + "gmscore version is "+item+ '\x1b[0m')
							#need color item 	print >> w , ('\x1b[2;32;41m' + "this device have wellbeing but gmscore lower than 17.7.85"+ '\x1b[0m')
								print >> w , ("gmscore version is "+item)
								print >> w , ("this device have wellbeing but gmscore lower than 17.7.85")
		except:
			pass

	####################




	comment("Fingerprint",'property','ro.build.fingerprint')
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
	
	print >> w , ""
	print >> w , "Default:Pass"
	print >> w , "Device:"	
	print >> w , "==================================================================="





	try:
		try:
			check_go = subprocess.check_output(str("adb -s "+ self.serialID +" shell getprop ro.com.google.gmsversion"), shell=True)[:-1]
			check_funding = subprocess.check_output(str('adb -s '+ self.serialID +' shell pm list features | grep -c "com.google.android.feature.GMSEXPRESS_PLUS_BUILD"'), shell=True)[:-1]
		except:
			pass
		if 'go' in check_go or 'GO' in check_go:
			
			go_check(self)
			
		
		if check_funding > 0 :
			
			express_plus(self)

	except:
		pass

	#run go fuding

	EEA_check()
	print >> w , "============================================================"
	print >> w , ""
	print >> w , "Please check broser intent is correct"
	print >> w , ""
	os.system(str("adb -s "+self.serialID+"  shell am start -a android.intent.action.VIEW -d http://google.com"))
	print >> w , ""
	print >> w , "===========================DF End============================="



	w.close()

	with open('/CTS_tool/CTSV/3PL_verifier/default_check/'+str(devicename)+"_"+time.strftime("%Y-%m-%d")+".txt", "r") as file:
		data = file.read()




	running_jub = "default_"+time.strftime("%Y-%m-%d")
	create(devicename,data,running_jub)
	


def openFolder(self):
	os.system("nautilus "+ self.config['path']['source'])

def screenShot(self):
	self.getselectserialID()
	print  "\n"+"============================screenshot============================"+"\n"
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
	print  "\n"+"==========================Fingerprint==========================="+"\n"
	print self.propertys['ro.build.fingerprint']
	print  "\n"+"================================================================"+"\n"


def install_apps(self):
	self.getselectserialID()
	print  "\n"+"===========================20 apps==========================="+"\n"
	if self.androidVersion is '8.0' or self.androidVersion is '7.1':
		target=21
	else:
		target=8
	for x in range(1,target):
			os.system(str("adb -s "+self.serialID+" install -r /CTS_tool/CTSV/default/test"+str(x)+".apk"))
	for y in range(1,target):
			time.sleep(1)
			os.system(str("adb -s "+self.serialID+"  shell am start -n com.example.pega3.test"+str(y)+"/.Test"+str(y)))
	print  "==================================================================="	


def uninstall_apps(self):
	self.getselectserialID()
	print  "=========================uninstall 20apps========================="+"\n"
	if self.androidVersion is '8.0' or self.androidVersion is '7.1':
		target=21
	else:
		target=8
	for x in range(1,target):
			os.system(str("adb -s "+self.serialID+" uninstall com.example.pega3.test"+str(x)))	
	print  "\n"+"===========================End==========================="+"\n"


def xlsx(self):
	self.getselectserialID()
	print  "\n"+"===========================xlsx==========================="+"\n"

	model = self.propertys['ro.product.model']
	fingerprint = self.propertys['ro.build.fingerprint']
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

	print  "==================================================================="	

def go_check(self):

	self.getselectserialID()

	devicename=subprocess.check_output(str("adb -s " + self.serialID + " shell getprop ro.build.product").split()).replace("\n","")
	w = open('/CTS_tool/CTSV/3PL_verifier/default_check/'+str(devicename)+"_"+time.strftime("%Y-%m-%d")+".txt", 'a')
	
	os.system('/CTS_tool/CTSV/3PL_verifier/GMS\ Express\ Plus\ test\ script\ -\ Android\ R/go_check_script.sh'+ " -s "+ self.serialID)
	
	with open('/CTS_tool/CTSV/3PL_verifier/GMS Express Plus test script - Android R/go_check_'+str(devicename)+"_"+time.strftime("%Y%m%d")+".log","r") as file:
		data = file.read()
		print >> w , "===========================go_check==========================="
		w.write(data)
		print >> w ,"==================================================================="
	
	w.close()

	print  "==================================================================="	

def express_plus(self):
	self.getselectserialID()
	#print self.androidVersion
	

	devicename=subprocess.check_output(str("adb -s " + self.serialID + " shell getprop ro.build.product").split()).replace("\n","")
	w = open('/CTS_tool/CTSV/3PL_verifier/default_check/'+str(devicename)+"_"+time.strftime("%Y-%m-%d")+".txt", 'a')
	

	
	if str(self.androidVersion) == '11' :
	
		os.system('/CTS_tool/CTSV/3PL_verifier/GMS\ Express\ Plus\ test\ script\ -\ Android\ R/Express_20201023.sh' + " -s "+ self.serialID)
	else :

		os.system('/CTS_tool/CTSV/3PL_verifier/GMS\ Express\ Plus\ test\ script\ -\ Android\ R/Express_20200116.sh' + " -s "+ self.serialID)

	with open("/CTS_tool/CTSV/3PL_verifier/GMS Express Plus test script - Android R/TestResult_" + str(devicename)+"_"+time.strftime("%Y-%m-%d")+".txt","r") as file:
		print >> w, " "
		data = file.read()

		w.write(data)
		print >>w , "==================================================================="
	running_jub="express_plus"+time.strftime("%Y-%m-%d")
#	create(devicename,data,running_jub)
	w.close()

	

	print  "==================================================================="	
def create(devicename,data,running_jub):
#创建一个顶级弹窗
	top = Toplevel()
	top.title(devicename+"_"+running_jub)
	mesListbox = Text(top)
	mesListbox.insert(END,data)
	mesListbox.pack()


def installVerifier (self):
	print  "\n=========================Install Verifier==========================\n"
	self.getselectserialID()
	sourse=self.config['path']['source']+self.androidVersion+"/android-cts-verifier-"+self.androidVersion+"_r"+self.config['version']["cts"+str(eval(self.androidVersion))]+"-linux_x86-"+self.deviceType+".zip"

	if os.path.exists(str(self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType)):
		pass
	else:
		if os.path.exists(sourse):
			print  "zip file exists, unzip now......\n"
			# sourse=config['path']['source']+androidVersion+"/android-cts-verifier-"+androidVersion+"_r"+config['version']["cts"+str(eval(androidVersion))]+"-linux_x86-"+deviceType+".zip"
			extract_to=self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType
			unzip=zipfile.ZipFile(sourse)
			unzip.extractall(extract_to)
			unzip.close
		else:
			print  "verifier zip is not exists"
			print  "please download from 'https://source.android.com/compatibility/cts/downloads'"
		
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
			print  "please install openCV  by yourself"
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

	print  "\n==================================================================="	


def adb39 (self):
	print  "\n=========================adb 39==========================\n"
	adb_path = subprocess.check_output("adb | grep Install", shell=True).splitlines()[0].replace('Installed as ','').replace('/platform-tools/adb','')
	os.system(str("rm -r "+adb_path+"/platform-tools"))
	os.system(str("cp -rp "+self.config['path']['source']+"ADB_platform_v39/platform-tools "+adb_path+'/platform-tools'))
	os.system(str("adb kill-server ; adb version ; adb start-server"))
	print  "\n==================================================================="	

def adb40 (self):
	print  "\n=========================adb 40==========================\n"
	adb_path = subprocess.check_output("adb | grep Install", shell=True).splitlines()[0].replace('Installed as ','').replace('/platform-tools/adb','')
	os.system(str("rm -r "+adb_path+"/platform-tools"))
	os.system(str("cp -rp "+self.config['path']['source']+"ADB_platform_v40/platform-tools "+adb_path+'/platform-tools'))
	os.system(str("adb kill-server ; adb version ; adb start-server"))
	print  "\n==================================================================="	

def adb41 (self):
	print  "\n=========================adb 41==========================\n"
	adb_path = subprocess.check_output("adb | grep Install", shell=True).splitlines()[0].replace('Installed as ','').replace('/platform-tools/adb','')
	os.system(str("rm -r "+adb_path+"/platform-tools"))
	os.system(str("cp -rp "+self.config['path']['source']+"ADB_platform_v41/platform-tools "+adb_path+'/platform-tools'))
	os.system(str("adb kill-server ; adb version ; adb start-server"))
	print  "\n==================================================================="	

def EEA_V2(self):
	self.getselectserialID()
	print " 請在OOBE時就登入 EEA test account"
	print  " 選擇google作為預設Search engine"
	print  " 打開USB debug後 >> 跑腳本"

	print  "Item E1"
	print   "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep  EEA  '))
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep  paid  '))
	print  "-------------------------------------------------------------------------------------\n"

	print  "Item E3"
	print   "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine  '))
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine_aga  '))
	print  "-------------------------------------------------------------------------------------\n"

	print  "Item E4"
	print   "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine  '))
	os.system(str("adb -s " +self.serialID+ ' shell settings get secure selected_search_engine_chrome  '))
	print  "-------------------------------------------------------------------------------------\n"


def Turkey(self):
	self.getselectserialID()

	print  "Item T1"
	print   "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep TR  '))
	os.system(str("adb -s " +self.serialID+ ' shell dumpsys package features | grep paid  '))
	print  "-------------------------------------------------------------------------------------\n"

	print  "Item T3"
	print   "*************************************************************************************"
	os.system(str("adb -s " +self.serialID+ ' shell content query --uri content://com.google.settings/partner | grep "client_id"  '))
	print  "-------------------------------------------------------------------------------------\n"


if __name__ == '__main__':
	os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
	
