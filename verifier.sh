#!/bin/bash
SFTP_SERVER="3pl-test.pegatroncorp.com"
SFTP_USER="jinny"
SFTP_PWD="Pega#3p1O207"

function update_from_sftp(){
# If happen "mirror: Fatal error: Host key verification failed."
# run 
# ssh  jinny@3pl-test.pegatroncorp.com
# Pega#3p1O207

	FILE=/CTS_tool/CTSV/3PL_verifier/config.ini
	if test -f "$FILE"; then
		##exsit
		lftp sftp://$SFTP_USER:$SFTP_PWD@$SFTP_SERVER -e  'mirror -n  /disk3/3pl/CTS_tool/CTSV /CTS_tool/CTSV --exclude-glob *.ini ; bye'
	else
		lftp sftp://$SFTP_USER:$SFTP_PWD@$SFTP_SERVER -e  'mirror -n  /disk3/3pl/CTS_tool/CTSV /CTS_tool/CTSV  ; bye'
	fi
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

update_from_sftp
check_pip
run
