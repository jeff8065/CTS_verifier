Getting Started:
1. Download and extract the testing script
2. Device setup
	- Factory reset the device or reflash the testing build
	- Connect with WiFi
	- Skip all steps in the device setup such as sim, wifi connect, screen lock
3. The testing scripts are not compatible with the default Mac terminal
4. The testing script requires python, please install python in your workstation for the steps below

To see which version of Python 3 you have installed, open a command prompt and run
$ python3 --version


If you are using Ubuntu 16.10 or newer, then you can easily install Python 3.6 with the following commands:
$ sudo apt-get update
$ sudo apt-get install python3.6


If you’re using another version of Ubuntu (e.g. the latest LTS release), we recommend using the deadsnakes PPA to install Python 3.6:
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.6

Running the scripts:
1. cd ~/GMS Express Plus test script
2. chmod +x Express_20200116.sh
3. ./Express_20200116.sh

Test result file will be created into GMS Express Plus test script folder

**The testing script is only for reference, you can use your own script too
