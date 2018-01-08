#!/usr/bin/python

import subprocess
import commands
import time

target_process = -1
(status, output) = commands.getstatusoutput('adb shell ps | grep com.miui.video')
for line in output.split('\n'):
    print line
    print line.split()[1]
    target_process = int(line.split()[1])

fileHandle = open('log.log', 'w')

p = subprocess.Popen("adb logcat -v threadtime", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
returncode = p.poll()
while returncode is None:
        line = p.stdout.readline()
        returncode = p.poll()
        line = line.strip()
        if line.split()[2] == 'of' or int(line.split()[2]) == target_process:
            print line
            fileHandle.write(line)
            fileHandle.write('\n')
print returncode
