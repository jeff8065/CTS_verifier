import xml.etree.ElementTree as ui
import os

#get_ui = os.system("adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/view.xml")
push_ui = os.system("adb pull sdcard/window_dump.xml")

#get_ui
push_ui
uidump = ui.parse('window_dump.xml')
root = uidump.getroot()

for node in root.iter("node"):
    if node.attrib['text'] == 'Google':
        bounds = node.attrib['bounds']

coords = ''
for coord in bounds:
    if coord.isdigit() == True:
        coords += coord
    elif coord == ',':
        coords += ' '
    elif coord == ']':
        coords += ' '

os.system("adb shell input tap {}".format(coords))
           
