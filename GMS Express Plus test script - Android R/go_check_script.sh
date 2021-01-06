#!/bin/bash
cd /CTS_tool/CTSV/3PL_verifier/"GMS Express Plus test script - Android R"/

function serialAndToolToArray(){
	
	while getopts "s:" option
	do
	
    	case "${option}" in
        
	        s)
		  for var in ${OPTARG}
		  do
			eval serial$i="$var"
			eval serialArray+=("$"serial$i)
			
			eval echo ${serialArray[$i]}
			echo "################go_check############"
			echo >> "===========================go_check===========================" >>  $name.log
			i=$((i+1))
			countDevice=$i
			#echo $countDevice
		  done	 
		;;
	
	
	        ?)
	        echo "未知参数"
	        exit 1;;	
	    esac
	done
	
	for((i=1;i<=countDevice;i=i+1))
		do
			serial_options+=("-s")
			eval serial_options+=("$"serial$((i-1)))
			#	echo ${serial_options[@]}
			
		done
	brand=$(adb -s ${serialArray[$1]} shell getprop ro.product.brand | sed 's/\r//' )
	name=$( adb -s ${serialArray[$1]} shell getprop ro.product.name | sed 's/\r//' )	
	today=$(date +"%Y%m%d")
	name="go_check_""$name"'_'"$today"

}

function Go_check(){

	echo " "
	echo "Data partition size"
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "flash storage size in GB       +  4    +  8    +  16   +"
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "User data partition size in GB +  1.5  +  5.5  +  12.7 +"
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

	adb -s ${serialArray[$1]} shell df -H

	echo " "
	echo "RAM Size"
	adb -s ${serialArray[$1]} shell  free -h | grep Mem

	echo " "
#	echo "Screen resolution 854x480"
	adb -s ${serialArray[$1]} shell wm size

#	echo " "
#	echo "Camera resolution 5m = 2560x1920"
#	adb -s ${serialArray[$1]} shell dumpsys media.camera | grep picture-size-value

	echo ""
	#rm $name.log
	for P in $(adb -s ${serialArray[$1]} shell pm list packages); do test -n "$(adb -s ${serialArray[$1]} shell dumpsys package ${P#package:} | grep -C3 "android.intent.category.LAUNCHER\"" | grep -C2  "android.intent.action.MAIN\"" )" && echo ${P#package:} >>  $name.log ; done
	#cat a.log
	exempt=(calculator
	calendar
	camera
	clock
	contacts
	dialer
	files
	gallery
	messaging
	music
	launcher
	settings
	)
	#for i in ${exempt[*]}
	#do
	#	echo $i
	#	#sed -i '/*$i*/d' a.log
	#	sed -i '0,/.*'$i'/{//d}' a.log
	#	sed -i '0,/.*'$i'/{//d}' a.log

	#done

	echo ""
	echo "total  headed apps"
	wc -l  < $name.log
	echo ""

	echo " "
	#FilesGo
	Search="FilesGo: "
	echo "For Files Go check you only have Files GO, if have other please let tam know"
	adb -s ${serialArray[$1]} shell am start -W -a android.os.storage.action.MANAGE_STORAGE -c android.intent.category.DEFAULT > /dev/null

}
serialAndToolToArray "$@"
rm $name.log
Go_check 2>>$name.log 1>>$name.log
