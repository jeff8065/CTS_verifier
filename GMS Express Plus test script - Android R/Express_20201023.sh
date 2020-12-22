#!/bin/bash
cd /CTS_tool/CTSV/3PL_verifier/"GMS Express Plus test script - Android R"/
passed=0
failed=0
skipped=0
meminfo_text=$(adb shell dumpsys meminfo)
start=$(date +%s.%N)

# Check GMS Express Plus flag
check_flag() {
	echo "[$(date)]" >> $testResult
	adb shell getprop | grep ro.build.fingerprint >> $testResult
	adb shell getprop | grep ro.build.version.release >> $testResult
	adb shell getprop | grep ro.com.google.gmsversion >> $testResult
	adb shell getprop | grep ro.build.version.security_patch >> $testResult

	test=(`adb shell getprop | grep "ro.base_build" | grep -c noah`)
	if [ $test = 1 ]; then
    	echo This is Express baseline, noah is set >> $testResult
    	echo This is Express baseline, noah is set 
	else 
    	echo "This is not Express baseline, noah flag not set (Optional for ODM/OEM device)" >> $testResult
    	echo "This is not Express baseline, noah flag not set (Optional for ODM/OEM device)"
	fi

	test=( `adb shell pm list features | grep -c com.google.android.feature.GMSEXPRESS_BUILD`)
	if [ $test = 1 ]; then
    	echo GMS Express Flag is set!!! >> $testResult
    	echo GMS Express Flag is set!!!
	else 
    	echo "Error!!! Do not have GMS Express baseline flag (Optional for ODM/OEM device)" >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Do not have GMS Express baseline flag (Optional for ODM/OEM device)"
	fi

	test=( `adb shell pm list features | grep -c com.google.android.feature.GMSEXPRESS_PLUS_BUILD`)
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo GMS Express PLUS Flag is set!!! >> $testResult
    	echo GMS Express PLUS Flag is set!!!
	else
    	failed=$((failed+=1))
    	echo "Error!!! Do not have GMS Express Plus flag" >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Do not have GMS Express Plus flag" 
	fi
	return $passed
}

check_smartspace() {
	echo
	echo Checking At a Glance Widget...
	echo >> $testResult
	echo At a Glance Widget: >> $testResult
	adb shell input keyevent 03
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test=(`grep -c com.google.android.googlequicksearchbox:id/smartspace_content window_dump.xml`)
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo At a Glance Widget is on DHS >> $testResult
    	echo At a Glance Widget is on DHS
	else
    	failed=$((failed+=1))
    	echo Error!!! At a Glance Widget is not on DHS >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) At a Glance Widget is not on DHS"
	fi

	rm window_dump.xml
}

check_google_dialer() {
	echo
	echo Checking Google Dialer...
	echo >> $testResult
	echo Google Dialer: >> $testResult
	test=( `adb shell pm list features | grep -c android.hardware.telephony` )
	if [ $test = 0 ]; then
		skipped=$((skipped+=1))
		echo Tablet does not requires to preload Google Dialer
		echo Tablet does not requires to preload Google Dialer >> $testResult
		return
	fi

	test=( `adb shell dumpsys role | grep -c com.google.android.dialer` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Dialer is preloaded and the only Dialer app >> $testResult
    	echo Google Dialer is preloaded and the only Dialer app
	else
    	failed=$((failed+=1))
    	echo "Error!!! Google Dialer is not preloaded or the only Dialer app(Waived if it is WiFi only tablet)" >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Dialer is not preloaded or the only Dialer app(Waived if it is WiFi only tablet)"
	fi

	sleep 2s
}

check_google_contacts() {
	echo
	echo Checking Google Contacts...
	echo >> $testResult
	echo Google Contacts: >> $testResult
	test=( `adb shell am start -W -a android.intent.action.VIEW content://contacts/people/ | grep -c com.google.android.contacts` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Contacts is preloaded and the only Contacts app >> $testResult
    	echo Google Contacts is preloaded and the only Contacts app
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Contacts is not preloaded or the only Contacts app >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Contacts is not preloaded or the only Contacts app"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.dialer
	sleep 2s
}

check_3P_OTA() {
	echo
	echo Checking 3P OTA Engine...
	echo >> $testResult
	echo 3P OTA Engine: >> $testResult
	ota1=( `adb shell pm list package -i | grep -c com.rock.gota` )
	ota2=( `adb shell pm list package -i | grep -c com.adups.fota` )
	ota3=( `adb shell pm list package -i | grep -c com.dtinfo.tools` )
	ota4=( `adb shell pm list package -i | grep -c com.xfota` )
	ota5=( `adb shell pm list package -i | grep -c com.redstone.ota.ui` )
	ota6=( `adb shell pm list package -i | grep -c com.adups.fota.sysoper` )
	ota7=( `adb shell pm list package -i | grep -c com.thundersoft.zdm` )
	ota8=( `adb shell pm list package -i | grep -c com.fota.digitime` )
	if [ $ota1 = 0 -a $ota2 = 0 -a $ota3 = 0 -a $ota4 = 0 -a $ota5 = 0 -a $ota6 = 0 -a $ota7 = 0 -a $ota8 = 0 ]; then
    	passed=$((passed+=1))
    	echo 3P OTA Engine is not using >> $testResult
    	echo 3P OTA Engine is not using
	else
    	failed=$((failed+=1))
    	echo Error!!! 3P OTA Engine is not using >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) 3P OTA Engine is not using"
	fi

	sleep 1s
}

# Check Assistant(Normal)
check_assistant() {
	echo
	echo Checking Google Assistant...
	echo >> $testResult
	echo Google Assistant: >> $testResult
	test=( `adb shell dumpsys role | grep -c com.google.android.googlequicksearchbox` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Assistant is the only assistant >> $testResult
    	echo Google Assistant is the only assistant
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Assistant is not the only assistant >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Assistant is not the only assistant"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.googlequicksearchbox
	sleep 2s

	# Check Assistant icon in DHS
	adb shell input keyevent 03
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test=(`grep -c Assistant window_dump.xml`)
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Assistant is on DHS for ROW build >> $testResult
    	echo Assistant is on DHS
	else
    	failed=$((failed+=1))
    	echo Error!!! Assistant is not on DHS for ROW build >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Assistant is not on DHS for ROW build"
	fi

	rm window_dump.xml
}

check_assistant_eea() {
	echo
	echo Checking Google Assistant...
	echo >> $testResult
	echo Google Assistant: >> $testResult
	test=( `adb shell dumpsys role | grep -c com.google.android.googlequicksearchbox` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Assistant is the only assistant >> $testResult
    	echo Google Assistant is the only assistant
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Assistant is not the only assistant >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Assistant is not the only assistant"
	fi

	sleep 2s

	# Check Assistant icon in DHS
	adb shell input keyevent 03
	adb shell input touchscreen swipe 600 600 100 600
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test=(`grep -c Assistant window_dump.xml`)
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Assistant icon is on screen +1 on EEA build >> $testResult
    	echo Assistant icon is on screen +1 on EEA build
	else
    	failed=$((failed+=1))
    	echo Error!!! Assistant icon is not on screen +1 on EEA build >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Assistant icon is not on screen +1 on EEA build"
	fi

	rm window_dump.xml
}

# Check Assistant Go
check_assistant_go() {
	echo
	echo Checking Google Assistant...
	echo >> $testResult
	echo Google Assistant: >> $testResult
	test=( `adb shell am start -W -a android.intent.action.ASSIST | grep -c com.google.android.apps.assistant` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Assistant is the only assistant >> $testResult
    	echo Google Assistant is the only assistant
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Assistant is not the only assistant >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Assistant is not the only assistant"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.apps.assistant
	sleep 2s
}

# Check Google Search
check_search() {
	echo
	echo Checking Google Search...
	echo >> $testResult
	echo Google Search: >> $testResult
	test=( `adb shell pm list packages -i | grep -c com.google.android.googlequicksearchbox` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Search is preloaded >> $testResult
    	echo Google Search is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Search is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Search is not preloaded"
	fi

	test=( `adb shell am start -W -a android.intent.action.WEB_SEARCH -e query wikipedia | grep -c com.google.android.googlequicksearchbox` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google search is the only search engine in the device >> $testResult
    	echo Google search is the only search engine in the device
	else
    	failed=$((failed+=1))
    	echo Error!!! Google search is not the only search engine in the device >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google search is not the only search engine in the device"
	fi

	sleep 3s
	adb shell am force-stop com.google.android.googlequicksearchbox
	sleep 1s
}

# Check Google Search(Go)
check_search_go() {
	echo
	echo Checking Google Search...
	echo >> $testResult
	echo Google Search: >> $testResult
	test=( `adb shell pm list packages -i | grep -c com.google.android.apps.searchlite` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Search is preloaded >> $testResult
    	echo Google Search is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Search is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Search is not preloaded"
	fi

	test=( `adb shell am start -W -a android.intent.action.WEB_SEARCH -e query wikipedia | grep -c com.google.android.apps.searchlite` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google search is the only search engine in the device >> $testResult
    	echo Google search is the only search engine in the device
	else
    	failed=$((failed+=1))
    	echo Error!!! Google search is not the only search engine in the device >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google search is not the only search engine in the device"
	fi

	sleep 3s
	adb shell am force-stop com.google.android.apps.searchlite
	sleep 1s
}

# Check Chrome
check_chrome() {
	# Back to DHS
	adb shell input keyevent 03

	# Check default browser
	test=( `adb shell dumpsys role | grep -c com.android.chrome` )
	if [ $test = 1 ]; then
   		passed=$((passed+=1))
    	echo Chrome is the default browser >> $testResult
    	echo Chrome is the default browser
	else
    	failed=$((failed+=1))
    	echo Error!!! Chrome is not the default browser >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Chrome is not the default browser"
	fi

	sleep 2s

	sleep 1s
	adb shell input keyevent 03
	# Check Chrome is at hotseat
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test1=(`xmllint /tmp/view.xml --xpath '//node[contains(@resource-id,"hotseat")]/node/node/@text' | grep -c Chrome`)
	test2=(`xmllint /tmp/view.xml --xpath '//node[contains(@resource-id,"hotseat")]/node/node/node/@text' | grep -c Chrome`)
	if [ $test1 = 1 -o $test2 = 1 ]; then
    	passed=$((passed+=1))
    	echo Chrome is at hotseat >> $testResult
    	echo Chrome is at hotseat
	else
    	failed=$((failed+=1))
    	echo Error!!! Chrome is not at hotseat >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Chrome is not at hotseat"
	fi

	rm window_dump.xml
}

# Check Android Messages(Normal/Go)
check_messages() {
	echo
	echo Checking Message app...
	echo >> $testResult
	echo Android Message: >> $testResult
	# Check Android Messages is preloaded

	test=( `adb shell pm list features | grep -c android.hardware.telephony` )
	if [ $test = 0 ]; then
		skipped=$((skipped+=1))
		echo Tablet does not requires to preload Android Message
		echo Tablet does not requires to preload Android Message >> $testResult
		return
	fi

	test=( `adb shell dumpsys role | grep -c com.google.android.apps.messaging` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Android Message is preloaded >> $testResult
    	echo Android Message is preloaded
	else
    	failed=$((failed+=1))
    	echo Android Message is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Android Message is not preloaded"
	fi

	sleep 1s
	adb shell input keyevent 03

	# Check Android Message is at the hotseat
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test1=(`xmllint /tmp/view.xml --xpath '//node[contains(@resource-id,"hotseat")]/node/node/@text' | grep -c Messages`)
	test2=(`xmllint /tmp/view.xml --xpath '//node[contains(@resource-id,"hotseat")]/node/node/node/@text' | grep -c Messages`)
	if [ $test1 = 1 -o $test2 = 1 ]; then
    	passed=$((passed+=1))
    	echo Messages is at hotseat >> $testResult
    	echo Messages is at hotseat
	else
    	failed=$((failed+=1))
    	echo Error!!! Messages is not at hotseat >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Messages is not at hotseat"
	fi

	rm window_dump.xml

	# Check Android Messages flag 
	test=( `adb shell getprop | grep ro.com.google.acsa | grep -c true` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Android Message ro.com.google.acsa is set >> $testResult
    	echo Android Message ro.com.google.acsa is set
	else
    	failed=$((failed+=1))
    	echo Error!!! Android Message ro.com.google.acsa is not set >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Android Message ro.com.google.acsa is not set"
	fi

	sleep 3s
}

# Check Google Photo
check_photo() {
	echo
	echo Checking Google Photo...
	echo >> $testResult
	echo Google Photo: >> $testResult

	test=( `adb shell dumpsys role | grep -c com.google.android.apps.photos` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google photo is the default app to review image. >> $testResult
    	echo Google photo is the default app to review image.
	else
    	failed=$((failed+=1))
    	echo Error!!! Google photo is not the default. >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google photo is not the default."
	fi

	sleep 3s
}

# Check Gallery Go
check_gallery_go() {
	echo
	echo Checking Gallery Go...
	echo >> $testResult
	echo Gallery Go: >> $testResult

	# Check Gallery Go is default
	test=( `adb shell dumpsys role | grep -c com.google.android.apps.photosgo` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Gallery Go is the default app to review image. >> $testResult
    	echo Gallery Go is the default app to review image.
	else
    	failed=$((failed+=1))
    	echo Error!!! Gallery Go is not the default. >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gallery Go is not the default."
	fi

	sleep 3s
}

# Check Google Calendar
check_calendar() {
	echo
	echo Checking Google Calendar...
	echo >> $testResult
	echo Google Calendar: >> $testResult
	test=( `adb shell pm list packages -i | grep -c com.google.android.calendar` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Calendar is preloaded >> $testResult
    	echo Google Calendar is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Calendar is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Calendar is not preloaded"
	fi

	test=( `adb shell am start -W -a android.intent.action.VIEW -d content://com.android.calendar/time/1410665898789 | grep -c com.google.android.calendar` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Google Calendar is the default Calendar >> $testResult
    	echo Google Calendar is the default Calendar
	else
    	failed=$((failed+=1))
    	echo Error!!! Google Calendar is not the default Calendar >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google Calendar is not the default Calendar"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.calendar
	sleep 1s
}

# Check Gmail
check_gmail() {
	echo
	echo Checking Gmail...
	echo >> $testResult
	echo Gmail: >> $testResult
	test=( `adb shell pm list packages -i | grep -c com.google.android.gm` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail is preloaded >> $testResult
    	echo Gmail is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail is not preloaded"
	fi

	sleep 1s

	test=( `adb shell am start -W -a android.intent.action.SENDTO -d mailto:someone@gmail.com | grep -c com.google.android.gm` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail is the default Email >> $testResult
    	echo Gmail is the default Email
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail is not the default Email >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail is not the default Email"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm | grep -c "android.permission.READ_CALENDAR: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can read calendar >> $testResult
    	echo Gmail can read calendar
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot read calendar >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot read calendar"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm | grep -c "android.permission.WRITE_CALENDAR: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can write calendar >> $testResult
    	echo Gmail can write calendar 
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot write calendar >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot write calendar"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm | grep -c "android.permission.READ_CONTACTS: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can read contacts >> $testResult
    	echo Gmail can read contacts
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot read contacts >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot read contacts"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm | grep -c "android.permission.WRITE_CONTACTS: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can write contact >> $testResult
    	echo Gmail can write contact
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot write contact >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot write contact"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.gm
	sleep 1s
}

# Check Gmail Go
check_gmail_go() {
	echo
	echo Checking Gmail...
	echo >> $testResult
	echo Gmail: >> $testResult
	test=( `adb shell pm list packages -i | grep -c com.google.android.gm.lite` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail is preloaded >> $testResult
    	echo Gmail is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail is not preloaded"
	fi

	sleep 1s

	test=( `adb shell am start -W -a android.intent.action.SENDTO -d mailto:someone@gmail.com | grep -c com.google.android.gm.lite` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail is the default Email >> $testResult
    	echo Gmail is the default Email
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail is not the default Email >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail is not the default Email"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm.lite | grep -c "android.permission.READ_CALENDAR: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can read calendar >> $testResult
    	echo Gmail can read calendar
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot read calendar >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot read calendar"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm.lite | grep -c "android.permission.WRITE_CALENDAR: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can write calendar >> $testResult
    	echo Gmail can write calendar 
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot write calendar >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot write calendar"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm.lite | grep -c "android.permission.READ_CONTACTS: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can read contacts >> $testResult
    	echo Gmail can read contacts
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot read contacts >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot read contacts"
	fi

	sleep 1s

	test=( `adb shell dumpsys package com.google.android.gm.lite | grep -c "android.permission.WRITE_CONTACTS: granted=true"` )
	if [ $test -ge 1 ]; then
    	passed=$((passed+=1))
    	echo Gmail can write contact >> $testResult
    	echo Gmail can write contact
	else
    	failed=$((failed+=1))
    	echo Error!!! Gmail cannot write contact >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gmail cannot write contact"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.gm.lite
	sleep 1s
}

# Check Files by Google
check_files_by_google() {
	echo
	echo Checking Files by Google...
	echo >> $testResult
	echo Files by Google: >> $testResult
	# Check Files by Google is preloaded
	test=( `adb shell pm list package -i | grep -c com.google.android.apps.nbu.files` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Files by Google is preloaded >> $testResult
    	echo Files by google is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Files by Google is not the only Files App >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Files by Google is not the only Files App"
	fi
	# Check File by Google is the only app for Files manager 
	test=( `adb shell am start -W -a android.os.storage.action.MANAGE_STORAGE | grep -c com.google.android.apps.nbu.files` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Files by Google is the only Files App >> $testResult
    	echo Files by Google is the only Files App
	else
    	failed=$((failed+=1))
    	echo Error!!! Files by Google is not the only Files App >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Files by Google is not the only Files App"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.apps.nbu.files
	sleep 1s
}

# Check Duo
check_duo() {
	echo
	echo Checking Duo...
	echo >> $testResult
	echo Duo: >> $testResult
	# Check Duo is preloaded
	test=( `adb shell pm list packages | grep -c com.google.android.apps.tachyon` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Duo is preloaded >> $testResult
    	echo Duo is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Duo is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Duo is not preloaded"
	fi

	sleep 1s
	adb shell am force-stop com.google.android.apps.tachyon
	sleep 1s

	adb shell input keyevent 03
	sleep 2s

	# Check Duo on DHS
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test=(`grep -c Duo window_dump.xml`)
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Duo is on DHS >> $testResult
    	echo Duo is on DHS
	else
    	failed=$((failed+=1))
    	echo Error!!! Duo is not on DHS. Please check it in Google folder or not for Go device >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Duo is not on DHS. Please check it in Google folder or not for Go device"
	fi

	rm window_dump.xml

	adb shell input keyevent 03
	sleep 2s
}

# Check Duo Go
check_duo_go() {
	echo
	echo Checking Duo Go...
	echo >> $testResult
	echo Duo: >> $testResult
	# Check Duo is preloaded
	test=( `adb shell pm list packages | grep -c com.google.android.apps.tachyon` )
	if [ $test = 1 ]; then
    	passed=$((passed+=1))
    	echo Duo Go is preloaded >> $testResult
    	echo Duo Go is preloaded
	else
    	failed=$((failed+=1))
    	echo Error!!! Duo Go is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Duo is not preloaded"
	fi
	sleep 1s
	adb shell am force-stop com.google.android.apps.tachyon
	sleep 1s

	adb shell input keyevent 03
	sleep 2s

	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test1=( `grep -c Duo window_dump.xml` )

	#Get Google Folder Bounds
	python3 get_coord.py

	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test2=( `grep -c Duo window_dump.xml` )

	if [ $test1 = 1 ] || [ $test2 = 1 ]; then
		passed=$((passed+=1))
    	echo Duo Go is on DHS or Google folder >> $testResult
    	echo Duo Go is on DHS or Google folder
    else
    	failed=$((failed+=1))
    	echo Error!!! Duo Go is not on DHS or Google folder >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Duo Go is not on DHS or Google folder"
    fi
	
	rm window_dump.xml

	adb shell input keyevent 03
	sleep 2s
}

#Check Gboard
check_gboard() {
	echo
	echo Checking Gboard...
	echo >> $testResult
	echo Gboard: >> $testResult
	
	# Check Gboard is preloaded
	test=( `adb shell settings get secure default_input_method | grep -c com.google.android.inputmethod` )
	if [ $test = 1 ]; then
		passed=$((passed+=1))
		echo Gboard is preloaded >> $testResult
		echo Gboard is preloaded
	else
		failed=$((failed+=1))
		echo Error!!! Gboard is not preloaded >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gboard is not preloaded"
    fi

    # Check Gboard is default IME
    test=( `adb shell ime list -a | grep mId | grep -v -c mId=com.google.android` )
    if [ $test = 0 ]; then
    	passed=$((passed+=1))
		echo Gboard is default IME >> $testResult
		echo Gboard is default IME
	else
		failed=$((failed+=1))
		echo Error!!! Gboard is not default IME >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Gboard is not default IME"
    fi
}

# Check Google Feed
check_google_feed() {
	echo
	echo Checking Google Feed -1 screen....
	echo >> $testResult
	echo Google Feed: >> $testResult
	adb shell input touchscreen swipe 10 600 600 600
	sleep 1s
	adb shell input touchscreen swipe 100 100 100 1000
	adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml
	adb pull sdcard/window_dump.xml
	test1=( `grep -c Updates window_dump.xml` )
	test2=( `grep -c sign_in_button window_dump.xml` )
	if [ $test1 = 1 -o $test2 ]; then
    	passed=$((passed+=1))
    	echo Google feed is in -1 screen >> $testResult
    	echo Google feed is in -1 screen
	else
    	failed=$((failed+=1))
    	echo Error!!! Google feed is in -1 screen >> $testResult
    	echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) Google feed is in -1 screen"
	fi
	rm window_dump.xml
}

# Main
echo
echo "$(tput bold)$(tput setaf 4)GMS Express Plus requirement testing script for Android R$(tput sgr0)"

# Check device is 1GB RAM or above
total_ram=$(echo "$meminfo_text"|grep -m 1 "Total RAM:"|cut -d '(' -f 1|cut -d ':' -f 2|awk '{$1=$1;print}'|tr -d ',kBK' || echo 0)
if [ $total_ram -lt 800000 ]; then
    echo "$(tput setaf 1)$(tput bold)Error!!!$(tput sgr0) GMS Express Plus Device requires 1GB RAM or above"
    exit
fi

productname=(`adb shell getprop | grep ro.build.product | awk -F ":" '{print$2}' | tr -d '[]'`)

testResult=TestResult_$productname.txt
rm -rf $testResult
echo "remove testResult"
touch $testResult
# Wake up device
adb shell input keyevent 224
adb shell input keyevent 82
adb shell input keyevent 03

# Checking whether Go device or not
test=( `adb shell pm list features | grep -c android.hardware.ram.low` )
isEEA=( `adb shell pm list features | grep -c com.google.android.feature.EEA_DEVICE` )
if [ $test = 0 -a $isEEA = 0 ]; then
    echo "$(tput setaf 4)$(tput bold)Testing GMS Express Plus ROW build requirement(Normal) now...$(tput sgr0)"
    # Check Express flag
	check_flag
	# Check Assistant setting
	check_assistant
	# Check Google Search
	check_search
	# Check Chrome
	check_chrome
	# Check Google Dialer
	check_google_dialer
	# check Google Contacts
	check_google_contacts
	# Check 3P OTA engine
	check_3P_OTA
	#check Smartspace
	check_smartspace
	# Check Calendar
	check_calendar
	# Check Gmail
	check_gmail
	# Check Files by Google
	check_files_by_google
	# Check Messages
	check_messages
	# Check Duo
	check_duo
	# Check Gboard
	check_gboard
	# Check Google feed
	check_google_feed
	# Check Google Photo
	adb shell input keyevent 224
	check_photo
elif [ $test = 0 -a $isEEA = 1 ]; then
	echo "$(tput setaf 4)$(tput bold)Testing GMS Express Plus EEA build requirement(Normal) now...$(tput sgr0)"
    # Check Express flag
	check_flag
	# Check Assistant setting for EEA build
	check_assistant_eea
	# Check Google Search
	check_search
	# Check Chrome
	check_chrome
	# Check Google Dialer
	check_google_dialer
	# check Google Contacts
	check_google_contacts
	# Check 3P OTA engine
	check_3P_OTA
	#check Smartspace
	check_smartspace
	# Check Calendar
	check_calendar
	# Check Gmail
	check_gmail
	# Check Files by Google
	check_files_by_google
	# Check Messages
	check_messages
	# Check Duo
	check_duo
	# Check Gboard
	check_gboard
	# Check Google feed
	check_google_feed
	# Check Google Photo
	adb shell input keyevent 224
	check_photo
fi

test=( `adb shell pm list features | grep -c android.hardware.ram.low` )
if [ $test = 1 -a $total_ram -lt 1700000 ]; then
	echo "$(tput setaf 4)$(tput bold)Testing GMS Express Plus Go(below 2GB RAM) requirement now...$(tput sgr0)"
    # Check Express flag
	check_flag
	# Check Assistant Go
	check_assistant_go
	# Check Google Search Go
	check_search_go
	# Check Chrome
	check_chrome
	# Check Google Dialer
	check_google_dialer
	# check Google Contacts
	check_google_contacts
	# Check 3P OTA engine
	check_3P_OTA
	# Check Calendar
	check_calendar
	# Check Gmail Go
	check_gmail_go
	# Check Files by Google
	check_files_by_google
	# Check Messages
	check_messages
	# Check Duo
	check_duo_go
	# Check Gboard
	check_gboard
	# Check gallery Photo
	adb shell input keyevent 224
	check_gallery_go
elif [ $test = 1 -a $total_ram -gt 1700000 ]; then
	echo "$(tput setaf 4)$(tput bold)Testing GMS Express Plus Go(2GB RAM) requirement now...$(tput sgr0)"
    # Check Express flag
	check_flag
	# Check Assistant Go
	check_assistant_go
	# Check Google Search Go
	check_search_go
	# Check Chrome
	check_chrome
	# Check Google Dialer
	check_google_dialer
	# check Google Contacts
	check_google_contacts
	# Check 3P OTA engine
	check_3P_OTA
	# Check Calendar
	check_calendar
	# Check Gmail(full version)
	check_gmail
	# Check Files by Google
	check_files_by_google
	# Check Messages
	check_messages
	# Check Duo
	check_duo_go
	# Check Gboard
	check_gboard
	# Check gallery Photo
	adb shell input keyevent 224
	check_gallery_go
fi

end=`date +%s`

end=$(date +%s.%N)
runtime=$(python -c "print(${end} - ${start})")
echo
echo -e "Total testing time is $runtime sec"
echo

echo "$(tput bold)$(tput setaf 4)GMS Express Plus Go device test is completed$(tput sgr0)"
echo -e "\nGMS Express requirement test result: $(tput setaf 2)$(tput bold)$passed Passed$(tput sgr0), $(tput setaf 1)$(tput bold)$failed Failed$(tput sgr0), $(tput setaf 4)$(tput bold)$skipped Skipped$(tput sgr0)\n"

echo -e "\nGMS Express Plus Requirement test result: $passed Passed, $failed Failed, $skipped Skipped" >> $testResult
