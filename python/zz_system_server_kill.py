#!/usr/bin/python

import commands
import time

(status, output) = commands.getstatusoutput('adb shell ps | grep system_server')
print 'Before kill\n' + output
commands.getstatusoutput('adb shell kill -9 ' + output.split()[1])
time.sleep(2)
(status, output) = commands.getstatusoutput('adb shell ps | grep system_server')
print 'After kill\n' + output