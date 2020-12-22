#!/bin/bash
cd /CTS_tool/CTSV/3PL_verifier
config=$(ls | grep config.ini)
chmod 755 /CTS_tool/CTSV/3PL_verifier/"GMS Express Plus test script - Android R"/.*
function gitsync()
{
	cd /CTS_tool/CTSV/3PL_verifier
	git init
	git remote add origin https://github.com/jeff8065/CTS_verifier.git
	git pull --all 
	git checkout -f remotes/origin/main
	sleep 5
	chmod 777 /CTS_tool/CTSV/3PL_verifier/*
#	chmod 777 /CTS_tool/CTSV/3PL_verifier/packages/*
#	chmod 777 /CTS_tool/CTSV/3PL_verifier/packages/packaging/*

}
function check_pip(){	
	if [[ -z $( pip list --format=legacy | grep openpyxl ) ]]; then
		echo "1"| sudo apt-get install python-openpyxl	
	fi
	if [[ -z $( pip list --format=legacy | grep configparser ) ]]; then
		echo "1"| sudo pip install configparser==3.3.0r2
	fi
}

function run(){
cd /CTS_tool/CTSV/3PL_verifier/
python  verifier.py
}

function addini()
{
echo "[version]

cts4.4 = 4 
cts5.0 = 10 
cts5.1 = 28 
cts6.0 = 32  
cts7.0 = 32 
cts7.1 = 27 
cts8.0 = 19 
cts8.1 = 18 
cts9.0 = 9 
cts10 = 3  
cts11 = 2 

[path]

source = /CTS_tool/CTSV/ 

" >config.ini

}
gitsync
if [ "$config" == "" ];then
echo "no!!!!!!!!!	"
addini
fi
#check_pip
run
