#!/usr/bin/python

import subprocess
import commands
import time

fileHandle = open('log.log', 'w')

p = subprocess.Popen("adb logcat -v threadtime", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
returncode = p.poll()
while returncode is None:
	line = p.stdout.readline()
	returncode = p.poll()
	line = line.strip()
	print line
	fileHandle.write(line)
    	fileHandle.write('\n')
print returncode
