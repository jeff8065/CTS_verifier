#!/usr/bin/env python2.7
# -*-coding: UTF-8 -*-
#Author : Leon Liao -2016/07
#Use : DefaultSettings and Verifier

import configparser
import subprocess
#import tkMessageBox as messagebox
import ttk
from Tkinter import *
from packages import DF_funtions, Remote_funtions, Ver_funtions, setting , TV_funtions


class Main(object):


	def checkList(self):
		deviceID = {}
		modelName = {}
		devices=subprocess.check_output('adb devices'.split())[25:]

		if "offline" in devices or "unauthorized" in devices:
			print "Please check"
			print " There is 'offline' or 'unauthorized' device, please check connect status"
			#messagebox.showerror("Please check"," There is 'offline' or 'unauthorized' device, please check connect status")

		i=0
		deviceAmount=len(devices.split())/2
		while i < deviceAmount:
			k = i * 2
			deviceID[i] = devices.split()[k]
			modelName[i] = subprocess.check_output(str("adb -s "+deviceID[i]+" shell getprop ro.product.model").split()).replace("\r\n","").strip().replace(" ","")
			i += 1
		self.li.delete (0, 20)
		for i in range(deviceAmount):
			self.li.insert(i, deviceID[i])
		self.li2.delete (0, 20)
		for i in range(deviceAmount):
			self.li2.insert(i, modelName[i])
		if self.li.size()==0:
			print "No device!!!"

	def getselectserialID(self):
		if self.li.size()==1:
			self.serialID = self.li.get(0)
		else:
			try:
				self.serialID = self.li.get(self.li.curselection()[0])
			except:
				self.serialID = self.li.get(self.li2.curselection()[0]) 

		self.property = subprocess.check_output("adb -s "+self.serialID+" shell getprop ", shell=True)
		self.features=subprocess.check_output(str("adb -s "+self.serialID+" shell pm list features").split()).replace("feature:","").splitlines()
		self.packages=subprocess.check_output(str("adb -s "+self.serialID+" shell pm list packages").split()).replace("package:","").splitlines()


		self.propertys={}
		for line in self.property.splitlines():
			name=line.split(':',1)[0].replace("[","").replace("]","")
			try:	
				key=line.split(':',1)[1].replace(" [","").replace("]","")
			except:
				pass	
			if len(key) > 0 :
				self.propertys[name]=key

		self.androidVersion = self.propertys['ro.build.version.release'][0:3]
		if self.androidVersion[0]=="9":
			self.androidVersion=str('9.0')
		if "x86" in self.propertys['ro.product.cpu.abi']:
			self.deviceType="x86"
		else:
			self.deviceType="arm"
		if "v8a" in self.propertys['ro.product.cpu.abi']:
			self.abiType="arm64-v8a"
		else:
			self.abiType="armeabi-v7a"
		
		self.install_cmd =  "adb -s "+ self.serialID +" install -r " + self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType+"/android-cts-verifier/"
		self.install_t_cmd =  "adb -s "+ self.serialID +" install -t " + self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType+"/android-cts-verifier/"
		self.push_cmd ="adb -s "+ self.serialID +" push  " + self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType+"/android-cts-verifier/"
		self.instant_cmd ="adb -s "+ self.serialID +" install -r --instant " + self.config['path']['source']+self.androidVersion+"/"+self.androidVersion+"r"+self.config['version']["cts"+str(eval(self.androidVersion))]+self.deviceType+"/android-cts-verifier/"
		self.uninstall_cmd =  "adb  -s "+ self.serialID +" uninstall "
	

	def __init__(self,master):

		class CaseConfigParser(configparser.ConfigParser):
			def optionxform(self, optionstr):
				return optionstr
		self.config = CaseConfigParser()
		self.config.read('config.ini')
		self.config.optionxform = str 


##########left frames##############
		self.left_frames = LabelFrame(master, width=450, height=240, text="select device")
		self.left_frames.grid(row=0, column=0 ,sticky=W+N)

		self.li = Listbox(self.left_frames,width=16, height=8)
		self.li.grid(row=0, column=0)
		self.li2 = Listbox(self.left_frames,width=16, height=8)
		self.li2.grid(row=0, column=1)

		checkButton = Button(self.left_frames, text="check devices", command= lambda: self.checkList())
		checkButton.grid(row=1, column=0 , columnspan=2 ,ipadx=1 ,ipady=3 , pady=3)


		self.label_1 = Label(self.left_frames, text="This tool verision\n" \
			+str(" 4.4 r"+self.config["version"]["cts4.4"])+ "\n" \
			+str(" 5.0 r"+self.config["version"]["cts5.0"])+ "\n" \
			+str(" 5.1 r"+self.config["version"]["cts5.1"])+ "\n" \
			+str(" 6.0 r"+self.config["version"]["cts6.0"])+ "\n" \
			+str(" 7.0 r"+self.config["version"]["cts7.0"]) )

		self.label_2=Label(self.left_frames, text="\n"\
			+str(" 7.1 r"+self.config["version"]["cts7.1"])+ "\n" \
			+str(" 8.0 r"+self.config["version"]["cts8.0"])+ "\n" \
			+str(" 8.1 r"+self.config["version"]["cts8.1"])+ "\n" \
			+str(" 9.0 r"+self.config["version"]["cts9.0"])+ "\n" \
			+str(" 10 r"+self.config["version"]["cts10"])+ "\n" \
			+str(" 11 r"+self.config["version"]["cts11"])  )


		self.label_1.grid(row=2, column=0)
		self.label_2.grid(row=2, column=1)
		settingButton = Button(self.left_frames, text = 'setting', command=lambda: setting.settingui(self))
		settingButton.grid(row=3, column=0)

		fp2Button = Button(self.left_frames, text= "FingerPrint", command=lambda: DF_funtions.checkfingerprint(self))
		fp2Button.grid(row=3, column=1)

########## right frames ############
		tab_parent = ttk.Notebook(master)
		Default_tab = ttk.Frame(tab_parent)
		Verfier_tab = ttk.Frame(tab_parent)
		Remote_tab = ttk.Frame(tab_parent)
		TV_tab = ttk.Frame(tab_parent)

		'''
		tab_list=list()
		item_list = self.config.items('sheet_sort')
		for item in item_list:
			tab_list.insert( int(item[1]),  str(item[0]))
		print tab_list
		
		for item in tab_list:
			tab_parent.add(eval(item),text= item.replace("_tab",""))
		'''
		
		tab_parent.add(Default_tab, text=" Default ")
		tab_parent.add(Verfier_tab, text=" Verifier ")
		tab_parent.add(Remote_tab, text=" Remote ")
		tab_parent.add(TV_tab, text=" TV ")

		tab_parent.grid(row=0, column=1, pady=5 ,sticky=W)


		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		######################## DF_tab ###########################




		default_funtion = LabelFrame(Default_tab, text="default setting")
		default_funtion.grid(row=0, column=0,sticky=N+S+E+W)
		Ver_funtion =  LabelFrame(Default_tab, text="verifer")
		Ver_funtion.grid(row=1, column=0,sticky=N+S+E+W)
		other_funtion = LabelFrame(Default_tab, text="other")
		other_funtion.grid(row=2, column=0,sticky=N+S+E+W)


		#####DF####
		defaultButton = Button(default_funtion, text="default_script", command=lambda: DF_funtions.defaultSettings(self))
		defaultButton.grid(row=0, column=0,ipadx=1 ,ipady=3 , pady=3, sticky=N+S+E+W)

		xlsxButton = Button(default_funtion, text="xlsx", command=lambda: DF_funtions.xlsx(self))
		xlsxButton.grid(row=0, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		install_appsButton = Button(default_funtion, text="install apps", command=lambda: DF_funtions.install_apps(self))
		install_appsButton.grid(row=1, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		uninstall_appsButton = Button(default_funtion, text="uninstall apps", command=lambda: DF_funtions.uninstall_apps(self))
		uninstall_appsButton.grid(row=1, column=1, ipadx=1, ipady=3, pady=3, sticky=N+S+E+W)

		EEA_V2Button = Button(default_funtion, text="EEA_V2", command=lambda: DF_funtions.EEA_V2(self))
		EEA_V2Button.grid(row=2, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		TurkeyButton = Button(default_funtion, text="Turkey", command=lambda: DF_funtions.Turkey(self))
		TurkeyButton.grid(row=2, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)


		##########verifer #######
		installVerifierButton = Button(Ver_funtion, text="install verifier", command=lambda: DF_funtions.installVerifier(self))
		installVerifierButton.grid(row=0, column=0,ipadx=1 ,ipady=3 , pady=3, sticky=N+S+E+W)

		##########other #########

#		fpButton = Button(other_funtion, text="fingerprint", command=lambda: DF_funtions.checkfingerprint(self))
#		fpButton.grid(row=0, column=0, ipadx=1, ipady=3, pady=3, sticky=N+S+E+W)

		screenshotButton = Button(other_funtion, text="screenshot", command=lambda: DF_funtions.screenShot(self))
		screenshotButton.grid(row=0, column=0,ipadx=1 ,ipady=3 , pady=3, sticky=N+S+E+W)

		openfolderButton = Button(other_funtion, text="openfolder", command=lambda: DF_funtions.openFolder(self) )
		openfolderButton.grid(row=0, column=1,ipadx=1 ,ipady=3 , pady=3, sticky=N+S+E+W)

#		testButton = Button(other_funtion, text="test", command=lambda: DF_funtions.test(self))
#		testButton.grid(row=1, column=1, ipadx=1, ipady=3, pady=3, sticky=N+S+E+W)

		adb39Button = Button(other_funtion, text="adb 39", command=lambda: DF_funtions.adb39(self))
		adb39Button.grid(row=1, column=0, ipadx=1, ipady=3, pady=3, sticky=N+S+E+W)

		adb40Button = Button(other_funtion, text="adb 40", command=lambda: DF_funtions.adb40(self))
		adb40Button.grid(row=1, column=1, ipadx=1, ipady=3, pady=3, sticky=N+S+E+W)

		adb41Button = Button(other_funtion, text="adb 41", command=lambda: DF_funtions.adb41(self))
		adb41Button.grid(row=1, column=2, ipadx=1, ipady=3, pady=3, sticky=N+S+E+W)	


		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		######################## Ver_tab ###########################


		install_funtion = LabelFrame(Verfier_tab, text="Verifier")
		install_funtion.grid(row=0, column=0,sticky=N+S+E+W)
		Administration_funtion = LabelFrame(Verfier_tab, text="Device admin")
		Administration_funtion.grid(row=1, column=0,sticky=N+S+E+W)
		BYOD_funtion = LabelFrame(Verfier_tab, text="BYOD area")
		BYOD_funtion.grid(row=2, column=0,sticky=N+S+E+W)
		Sensors_funtion = LabelFrame(Verfier_tab, text="Sensors")
		Sensors_funtion.grid(row=3, column=0,sticky=N+S+E+W)
		Vother_funtion = LabelFrame(Verfier_tab, text="Other")
		Vother_funtion.grid(row=4, column=0,sticky=N+S+E+W)



		##install
		installVerifier2Button = Button(install_funtion, text="install verifier", command=lambda: DF_funtions.installVerifier(self))
		installVerifier2Button.grid(row=0, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)


		#######Administration#########
		Usb_devuggingButton = Button(Administration_funtion, text="UsbDebugDialog ", command=lambda: Ver_funtions.USB_Debugging(self))
		Usb_devuggingButton.grid(row=1, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		remove_adminButton = Button(Administration_funtion, text="remove_admin", command=lambda: Ver_funtions.remove_admin(self))
		remove_adminButton.grid(row=1, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)


		#######BYOD#########
		BYOD_VPN_23Button = Button(BYOD_funtion, text="VPN_23", command=lambda: Ver_funtions.BYOD_VPN_23(self))
		BYOD_VPN_23Button.grid(row=0, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		BYOD_VPN_24Button = Button(BYOD_funtion, text="VPN_24", command=lambda: Ver_funtions.BYOD_VPN_24(self))
		BYOD_VPN_24Button.grid(row=0, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		BYOD_VPN_NAOButton = Button(BYOD_funtion, text="VPN_NAO", command=lambda: Ver_funtions.BYOD_VPN_NAO(self))
		BYOD_VPN_NAOButton.grid(row=0, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)



		deviceOwnerButton = Button(BYOD_funtion, text="DeviceOwner", command=lambda: Ver_funtions.deviceOwner(self))
		deviceOwnerButton.grid(row=1, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		newOwnerButton = Button(BYOD_funtion, text="OS8_Owner", command=lambda: Ver_funtions.newOwner(self))
		newOwnerButton.grid(row=1, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)


		#######sensors#########
		UIDButton = Button(Sensors_funtion, text="UID set ", command=lambda: Ver_funtions.UID(self))
		UIDButton.grid(row=0, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		UIDButton2 = Button(Sensors_funtion, text="UID reset ", command=lambda: Ver_funtions.UID2(self))
		UIDButton2.grid(row=0, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		CompassButton = Button(Sensors_funtion, text="Compass", command=lambda: Ver_funtions.CompassButton(self))
		CompassButton.grid(row=0, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		###########Vother_funtion########
		bmgrButton = Button(Vother_funtion, text="Bmgr ", command=lambda: Ver_funtions.bmgr_run(self))
		bmgrButton.grid(row=0, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		PerimissionButton = Button(Vother_funtion, text="Perimission", command=lambda: Ver_funtions.Perimission(self))
		PerimissionButton.grid(row=0, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		PullButton = Button(Vother_funtion, text="Pull report", command=lambda: Ver_funtions.Pull(self))
		PullButton.grid(row=0, column=2, ipadx=2, ipady=3, pady=3,sticky=N+S+E+W)




		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		######################## Remote_tab ###########################
		upButton = Button(Remote_tab, text="Up ", command=lambda: Remote_funtions.up(self))
		upButton.grid(row=0, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		leftButton = Button(Remote_tab, text="Left ", command=lambda: Remote_funtions.left(self))
		leftButton.grid(row=1 ,column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		downButton = Button(Remote_tab, text="Down ", command=lambda: Remote_funtions.down(self))
		downButton.grid(row=2, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		rightButton = Button(Remote_tab, text="Right ", command=lambda: Remote_funtions.right(self))
		rightButton.grid(row=1, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		enterButton = Button(Remote_tab, text="Enter ", command=lambda: Remote_funtions.enter(self))
		enterButton.grid(row=1, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)        

		backButton = Button(Remote_tab, text="Back ", command=lambda: Remote_funtions.back(self))
		backButton.grid(row=3, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		homeButton = Button(Remote_tab, text="Home ", command=lambda: Remote_funtions.home(self))
		homeButton.grid(row=3, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		recentButton = Button(Remote_tab, text="Recent ", command=lambda: Remote_funtions.recent(self))
		recentButton.grid(row=3, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)


		self.entryText = Entry(Remote_tab)
		self.entryText.grid(row=4, column=0,columnspan=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		sendtextButton = Button(Remote_tab, text="Send ", command=lambda: Remote_funtions.text(self))
		sendtextButton.grid(row=4, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		self.pressText = Entry(Remote_tab)
		self.pressText.grid(row=5, column=0,columnspan=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)
		presstextButton = Button(Remote_tab, text="Press ", command=lambda: Remote_funtions.presstext(self))
		presstextButton.grid(row=5, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		self.loopValue = StringVar() 
		chkExample = Checkbutton(Remote_tab, text='loop', var=self.loopValue) 
		chkExample.grid(row=5, column=3, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		opensettingButton = Button(Remote_tab, text= "setting", command=lambda: Remote_funtions.opensetting(self))
		opensettingButton.grid(row=6, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		kill_recentButton = Button(Remote_tab, text= "kill recent", command=lambda: Remote_funtions.kill_recent(self))
		kill_recentButton.grid(row=6, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)


		cardockButton = Button(Remote_tab, text= "Car Dock", command=lambda: Remote_funtions.home(self))
		cardockButton.grid(row=7, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		stayawakeButton = Button(Remote_tab, text= "Stay Awake", command=lambda: Remote_funtions.stayawake(self))
		stayawakeButton.grid(row=7, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		##########################################################
		######################## TV_tab ###########################

		TV_propertyButton = Button( TV_tab, text= "property", command=lambda: TV_funtions.property_check(self))
		TV_propertyButton.grid(row=0, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		TV_Exo_appButton = Button( TV_tab, text= "Exo_app", command=lambda: TV_funtions.Exo_app(self))
		TV_Exo_appButton.grid(row=0, column=1, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		TV_apksButton = Button( TV_tab, text= "APKs", command=lambda: TV_funtions.install_apks(self))
		TV_apksButton.grid(row=0, column=2, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)

		YT_Button = Button( TV_tab, text= "YT", command=lambda: TV_funtions.test(self))
		YT_Button.grid(row=1, column=0, ipadx=1, ipady=3, pady=3,sticky=N+S+E+W)



def main():
	self = Tk()
	app = Main(self)
	self.title("3PL tool")
#	self.geometry("600x450+30+30")
	self.mainloop()

if __name__ == '__main__':
	main()
