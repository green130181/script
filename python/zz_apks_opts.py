#!/usr/bin/python
import sys
import commands
import os
import getopt
import re
import ConfigParser

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

    # for arg in sys.argv:
    #     print arg
    # list = GetFileList(APPS_PATH, [])
    #     for e in list:
    #         print 'adb install ' + e
    #         (status, output) = commands.getstatusoutput('adb install ' + e)
    #         if output.find('Failure') != -1:
    #             print 'result:' + str(status)
    #             print 'output:' + output
    #             sys.exit(-1)
    #         else:
    #             print 'result:' + str(status)
APPS_PATH = '/home/mi/work/h2a_art_dalvik/new/apps/'
AAPT = '/home/mi/Android/Sdk/build-tools/24.0.3/aapt'
CMD_PACKAGE_INFO = AAPT + ' dump badging "%s" | head -n 1'
PACKAGE_INFO_REGEX = re.compile(r"package: name='(.*)' versionCode='(.*)' versionName='(.*)'", re.I)
DEVICE = '-1'
ADB = '/home/mi/Android/Sdk//platform-tools/adb '

def get_apk_name(app_file):
    apk_infos = {}
    # get package name and version_name & version_code
    try:
        (status, output) = commands.getstatusoutput(CMD_PACKAGE_INFO % app_file)
        print output
        m = PACKAGE_INFO_REGEX.search(output)
        if m:
            apk_infos['package_name'] = m.group(1)
            apk_infos['version_code'] = int(m.group(2) or 0)
            apk_infos['version_name'] = m.group(3)
            return apk_infos['package_name']

    except Exception, e:
        'get package info failed, cmd: %s, error: %s' % (CMD_PACKAGE_INFO % file_path, e)
        return None

def Usage(python_script_name):
    print python_script_name + ' usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-d, --dir: apk directory'
    print '-i, --install: install apks in directory'
    print '-u, --uninstall: uninstall apks in directory'


def Version(python_script_name):
    print python_script_name + ' 1.0.0.0.1'


def Install(args):
    print 'Start install, %s apks' % args
    file_list = GetFileList(args, [])

    for e in file_list:
        print ADB, 'install', e
        (status, output) = commands.getstatusoutput(ADB + ' install ' + e)
        if output.find('Failure') != -1:
            print 'result:' + str(status)
            print 'output:' + output
            sys.exit(-1)
        else:
            print 'result:' + str(status)

def Uninstall(args):
    print 'Start uninstall, %s apks' % args
    file_list = GetFileList(args, [])

    for e in file_list:
        package_name = get_apk_name(e)
        if package_name == None:
            print 'Get app %s package info failed' % e
            sys.exit(-1)
        print ADB + ' uninstall ' + package_name
        (status, output) = commands.getstatusoutput(ADB + ' uninstall ' + package_name)
        if output.find('Failure') != -1:
            print 'result:' + str(status)
            print 'output:' + output
        else:
            print 'result:' + str(status)

def main(argv):
    #cf = ConfigParser.ConfigParser()
    #cf.read('/home/mi/bin/py_script.conf')
    #global DEVICE
    #global ADB
    #DEVICE = cf.get('devices', 'active')
    #ADB = '/home/mi/Android/Sdk//platform-tools/adb -s ' + DEVICE
    ADB = '/home/mi/Android/Sdk//platform-tools/adb '
    print 'Operate with device', DEVICE
    if len(argv) < 2:
        Usage(argv[0])
        sys.exit(1)
    try:
        opts, args = getopt.getopt(argv[1:], 'd:vhiu', ['dir=', 'version', 'help', 'install', 'uninstall'])
    except getopt.GetoptError, err:
        print str(err)
        Usage(argv[0])
        sys.exit(2)

    apk_dir = ''
    opt = ''
    print opts
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage(argv[0])
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version(argv[0])
            sys.exit(0)
        elif o in ('-d', '--dir'):
            apk_dir = a
        elif o in ('-i', '--install'):
            opt = 'install'
        elif o in ('-u', '--uninstall'):
            opt = 'uninstall'
        else:
            print 'unhandled option'
            sys.exit(3)

    # print apk_dir,opt
    if apk_dir == '' or opt == '':
        Usage(argv[0])
        sys.exit(1)
    if opt == 'install':
        Install(apk_dir)
    elif opt == 'uninstall':
        Uninstall(apk_dir)

if __name__ == '__main__':
    main(sys.argv)
