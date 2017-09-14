import sys
import re
# import scanf
if __name__ == '__main__':
    if sys.argv.__len__() != 2:
        print 'Usage: TestJumpInstruction.py filename'
        sys.exit(0)
    filename = sys.argv[1]
    print 'analysis', filename

    #input = 'CODE: (code_offset = 0x0297c091 size_offset = 0x0297c08c size = 122)...'
    codeLengthpattern = re.compile(ur'size=\d+', re.S)
    startAddrPattern = re.compile(ur'0[xX][0-9a-fA-F]*', re.S)
    codeOverPattern = re.compile(ur'^\d+:', re.S)
    instOffsetPattern = re.compile(ur'\(0[xX][0-9a-fA-F]*\)$', re.S)

    file = open(filename, 'r')
    counter = 0
    analysis = False
    startAddr = 0
    endAddr = 0

    for (linenum, line) in enumerate(file):
        tmpstr = line.strip()

        # if counter > 5:
        #     break

        if analysis == True:
            find = codeOverPattern.search(tmpstr)
            if find != None:
                if find.group().__len__() > 0:
                    print 'Line Number :', linenum + 1, 'next line is \n', tmpstr,  '\n analysis over pass============'
                    analysis = False
                    continue

        #Find first code line
        index = tmpstr.find('CODE:')
        if index == 0:
            analysis = True
            counter+=1
            # find native code start
            print 'Line number ', linenum + 1, tmpstr

            startAddr = int(startAddrPattern.search(tmpstr).group().strip(), 16)
            codeLength = int(codeLengthpattern.search(tmpstr).group().strip()[5:])
            startAddr -= 1
            endAddr = startAddr + codeLength
            print hex(startAddr), '---', hex(endAddr)
            continue
        # Check instOffset
        findInstOffset = instOffsetPattern.search(tmpstr)
        if findInstOffset != None:
            print 'Line Number :', linenum + 1, 'find inst offset ***** ', tmpstr
            jmpAddr = int(findInstOffset.group()[1:-1], 16)
            if jmpAddr > endAddr or jmpAddr < startAddr:
                print 'Line Number :', linenum + 1, 'jump out current function'

    file.close()

