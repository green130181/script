#!/usr/bin/python

import commands
import time

(status, output) = commands.getstatusoutput('adb shell ps | grep zygote')
for line in output.split('\n'):
    print line
    commands.getstatusoutput('adb shell kill -9 ' + line.split()[1])
    print line.split()[1]
