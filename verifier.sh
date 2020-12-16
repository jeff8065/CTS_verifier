#!/bin/bash
function gitsync()
{
	cd /CTS_tool/CTSV/3PL_verifier
	git init
	git remote add origin https://github.com/jeff8065/CTS_verifier.git
	git pull --all 
	git checkout -f remotes/origin/main
	sleep 5

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

gitsync
echo "1"| sudo chmod 755 /CTS_tool/CTSV/3PL_verifier/*

#check_pip
run
