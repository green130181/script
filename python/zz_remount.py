#!/usr/bin/python

import commands
import time

(status, output) = commands.getstatusoutput('adb root && adb wait-for-device && adb remount')
print status, output
