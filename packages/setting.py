#!/usr/bin/env python2.7
# -*-coding: UTF-8 -*-
#Author : Leon Liao 

from Tkinter import *
import ttk ,os
import configparser


def settingui(self):
	def save():
		print "============    new version   ============="
		for sSection in total_section:
			if sSection == "version":
				for item in config.items(sSection):
					print item[0]+" : "+d[ "entry" + item[0] ].get()
					config['version'][item[0]] =  d[ "entry" + item[0] ].get()
		with open('config.ini', 'w') as configfile:    # save
			config.write(configfile)
		self.config.read('config.ini')
		self.label_1.destroy()
		self.label_2.destroy()

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
			+str(" 10 r"+self.config["version"]["cts10"]) )
		self.label_1.grid(row=2, column=0)
		self.label_2.grid(row=2, column=1)
		print "========================="


	master = Tk()
	#master.minsize(300,200)
	master.title("setting")
	

	config = configparser.ConfigParser()
	config.read('config.ini')
	total_section = config.sections()
	d = {}
	i = 0 
	for sSection in total_section:
		if sSection == "version":
			for item in config.items(sSection):
				#print "key = %s, valule = %s" % (item[0], item[1])
				d["labal" +item[0]] = Label(master, text= item[0])
				d["labal" +item[0]] .grid(row=i, column=0, ipadx=1,sticky=N+S+E+W)
				v = StringVar(master, value=self.config['version'][item[0]])
				d[ "entry" + item[0] ] = Entry(master,textvariable=v, width=10)
				d[ "entry" + item[0] ] .grid(row=i, column=1, ipadx=1,sticky=N+S+E+W)
				i=i+1
		"""
		if sSection == "path":
			for item in config.items(sSection):
				d["labal" +item[0]] = Label(master, text= item[0])
				d["labal" +item[0]] .grid(row=i, column=0, ipadx=1,sticky=N+S+E+W)
				v = StringVar(master, value=self.config['path'][item[0]])
				d[ "entry" + item[0] ] = Entry(master,textvariable=v, width=15)
				d[ "entry" + item[0] ] .grid(row=i, column=1, ipadx=1,sticky=N+S+E+W)
				i=i+1
		"""

		saveButton = Button(master, text = 'save', command=lambda: save())
		saveButton.grid(row=2, column=2)
		exitButton = Button(master, text = 'exit', command=lambda: master.destroy())
		exitButton.grid(row=4, column=2)
		#sourceLabel = Label(master, text="default : /CTS_tool/CTSV/")
		#sourceLabel.grid(row=10, column=2)


	mainloop()

if __name__ == '__main__':	
	os.system("python /CTS_tool/CTSV/3PL_verifier/verifier.py")
	