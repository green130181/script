#coding=utf-8

#gdb.execute("hbreak gdb_sample/gdb-sample.c :213")
#gdb.breakpoint(gdb.BP_HARDWARE_WATCHPOINT, "gdb_sample/gdb-sample.c :213")

# move.py
# 1. 导入gdb模块来访问gdb提供的python接口
import gdb
import commands
import ConfigParser

config_filepath = r'/home/mi/bin/gdb_script.conf'
breakpoint_start = 2
# 2. 用户自定义命令需要继承自gdb.Command类
class Move(gdb.Command):

    # 3. docstring里面的文本是不是很眼熟？gdb会提取该类的__doc__属性作为对应命令的文档
    """Move breakpoint
    Usage: mv old_breakpoint_num new_breakpoint
    Example:
        (gdb) mv 1 binary_search -- move breakpoint 1 to `b binary_search`
    """

    def __init__(self):
        # 4. 在构造函数中注册该命令的名字
        super(self.__class__, self).__init__("mv", gdb.COMMAND_USER)

    # 5. 在invoke方法中实现该自定义命令具体的功能
    # args表示该命令后面所衔接的参数，这里通过string_to_argv转换成数组
    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 2:
            raise gdb.GdbError('输入参数数目不对，help mv以获得用法')
        # 6. 使用gdb.execute来执行具体的命令
        gdb.execute('delete ' + argv[0])
        gdb.execute('break ' + argv[1])

# 7. 向gdb会话注册该自定义命令
Move()


def getaddress(logfile, address_dict):
    print 'in getaddress'
    index = 0
    baseaddr = 0
    for line in open(logfile, 'r'):
        #print line
        proc_startString = line.strip()
        if len(proc_startString) > 0:
            #print proc_startString.split(":")
            if proc_startString.split(":")[3] == "PrepareEntryPoint OK entrypoint":
                baseaddr = int(proc_startString.split(":")[4].split()[0], 16)
                #print baseaddr
            elif proc_startString.split(":")[3] == "BreakpointAtOffset":
                address_dict[index] = baseaddr + int(proc_startString.split(":")[4], 16)
                index += 1

# delete breakpoints 1-10

def reinsert_hw_breadpoint():
    print "reinsert_hw_breadpoint"
    cp = ConfigParser.SafeConfigParser()
    cp.read(config_filepath)
    start = int(cp.get('hwbreakpoint', 'start'))
    hw_number = int(cp.get('hwbreakpoint', 'hw_number'))
    breakpoint_number = int(cp.get('hwbreakpoint', 'breakpoint_number'))

    for index in range(breakpoint_number):
        gdb.execute("disable breakpoints " + str(index + breakpoint_start))

    range_length = 0
        # out of range back
    if start >= breakpoint_number:
        start = 0

    range_length = min(breakpoint_number - start, hw_number)

    print 'start:', start, 'range_length:', range_length
    for index in range(start, range_length):
        print 'gdb.execute("enable breakpoints "' + str(index + breakpoint_start) + ')'
        gdb.execute("enable breakpoints " + str(index + breakpoint_start))
        if (index + 1) == range_length:
            print "brk_commands_with_reinsert_hwpoint " + str(index + breakpoint_start)
            gdb.execute("brk_commands_with_reinsert_hwpoint " + str(index + breakpoint_start))
        else:
            print "brk_commands " + str(index + breakpoint_start)
            gdb.execute("brk_commands " + str(index + breakpoint_start))
        # gdb.execute("commands")
        # gdb.execute("info registers")
        # if (index + 1) == range_length:
        #     gdb.execute("zz_reinsert_hw_breadpoint")
        # gdb.execute("continue")
        # gdb.execute("end")

    cp.set('hwbreakpoint', 'start', str(start))
    cp.write(open(config_filepath, 'r+'))

class zz_reinsert_hw_breadpoint(gdb.Command):
    def __init__(self):
        # 4. 在构造函数中注册该命令的名字
        super(self.__class__, self).__init__("zz_reinsert_hw_breadpoint", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        reinsert_hw_breadpoint()

zz_reinsert_hw_breadpoint()

# 2. 用户自定义命令需要继承自gdb.Command类
class zz_main(gdb.Command):
    def __init__(self):
        # 4. 在构造函数中注册该命令的名字
        super(self.__class__, self).__init__("zz_main", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        gdb.execute("brk_prepare")

        (status, output) = commands.getstatusoutput(
            'adb pull /data/data/com.example.hellojni/cache/test.log /home/mi/bin/test.log')
        print status, output
        address_dict = {}
        getaddress("/home/mi/bin/test.log", address_dict)
        print 'find ', len(address_dict), 'breakpoint'

        for address in address_dict:
            print "hbreak *" + str(address_dict[address])
            gdb.execute("hbreak *" + str(address_dict[address]))

        cp = ConfigParser.SafeConfigParser()
        cp.read(config_filepath)
        cp.set('hwbreakpoint', 'start', "0")
        cp.set('hwbreakpoint', 'hw_number', "8")
        cp.set('hwbreakpoint', 'breakpoint_number', str(len(address_dict)))
        cp.write(open(config_filepath, 'r+'))

        reinsert_hw_breadpoint()
        # gdb.execute("hbreak gdb_sample/gdb-sample.c :213")
        # gdb.execute("brk_commands")
        # gdb.execute("hbreak gdb_sample/gdb-sample.c :220")
        # gdb.execute("brk_commands")
        # gdb.execute("hbreak gdb_sample/gdb-sample.c :131")
        # gdb.execute("brk_commands")

# 7. 向gdb会话注册该自定义命令
zz_main()

#if __name__ == '__main__':
    # (status, output) = commands.getstatusoutput('adb pull /data/data/com.example.hellojni/cache/test.log /home/mi/bin/test.log')
    # print status, output
    # getaddress("/home/mi/test.log", g_address_dict)
    # print g_address_dict
