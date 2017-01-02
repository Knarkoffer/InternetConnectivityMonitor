#-------------------------------------------------------------------------------
# Project	: 381
# Language	: Python
# Name		: Internet Connectivity Monitor
# Purpose	: A small script I use to make sure I immediately know when my internet connection goes down.
#			  Very handy when playing online or talking with people on TeamSpeak/Mumble/Skype
#
# Version	: 26
# Authors   : Knarkoffer
# Created   : 2016
# Site		: https://github.com/Knarkoffer/
# Licence   : MIT
#-------------------------------------------------------------------------------

import subprocess
import time
import winsound

# <GLOBAL VARIABLES>

# Configurables:
targetDomain = 'sunet.se' # This is the domain we'll send the ping-query to
timeIntervall = 1 # The time between each check (in seconds), I've set this to one second to quickly get informed
blnSoundEnabled = True

# Other:
blnStarted = False
blnConnected = False
blnDoubleDot = False
intTotalTimeoutCounter = 0
intTimeOutCounter = 0
starttime=time.time()

# </GLOBAL VARIABLES>

def PlayAudioFile(strAudioFilePath):
	
	winsound.PlaySound(strAudioFilePath,winsound.SND_FILENAME)
#


def run_command(command):
	
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return iter(p.stdout.readline, b'')
#


def ConnectionLost():
	
	print('Connection lost!')
	
	# If sounds are enabled, plays the "USB Disconnected"-sound
	if blnSoundEnabled:
		PlayAudioFile('C:\Windows\Media\Windows Hardware Remove.wav')
	#
#


def ConnectionRestored():
	
	global intTimeOutCounter
	global intTotalTimeoutCounter
	global blnStarted
	
	if blnStarted:
		
		# Total timeout calculator
		intTotalTimeoutCounter = intTotalTimeoutCounter + intTimeOutCounter

		totalTimeOutSeconds = intTotalTimeoutCounter % 60
		totalTimeOutMinutes = int((intTotalTimeoutCounter - totalTimeOutSeconds) / 60)

		print('Connection restored after ' + str(intTimeOutCounter) + ' seconds!' + '\n' + '(A total of ' + str(totalTimeOutMinutes) + ' minutes and ' + str(totalTimeOutSeconds) + ' seconds of outage)')
		
		# If sounds are enabled, plays the "USB Connected"-sound
		if blnSoundEnabled:
			PlayAudioFile('C:\Windows\Media\Windows Hardware Insert.wav')
		#
		
		intTimeOutCounter = 0
	
	blnStarted = True
#


def CheckConnection():
	
	global blnDoubleDot
	global blnConnected
	global intTimeOutCounter
	
	command = 'ping -n 1 ' + targetDomain
	
	for line in run_command(command):
		
		line = str(line.decode("utf-8"))
		
		if 'Reply from ' in line:
			
			if not blnConnected:
				
				ConnectionRestored()
				blnConnected = True
			#
			
		elif ('Request timed out.' in line) or ('General failure.' in line) or ('Ping request could not find host ' in line):
			
			if blnConnected:
				ConnectionLost()
				blnConnected = False
			#
		#
	#
	
	if blnConnected:
		if blnDoubleDot:
			print('Connected..')
			blnDoubleDot = False
		else:
			print('Connected.')
			blnDoubleDot = True
		#
		
	else:
		if blnDoubleDot:
			print('Disconnected..')
			blnDoubleDot = False
		else:
			print('Disconnected.')
			blnDoubleDot = True
		#
		
		intTimeOutCounter = intTimeOutCounter + 1
	#
#


while True:
	CheckConnection()
	time.sleep(timeIntervall - ((time.time() - starttime) % timeIntervall))
#

