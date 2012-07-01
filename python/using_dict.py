#!/usr/bin/python
# Filename: using_dict.py

# 'ab' is short for 'a'ddress'b'ook

ab = {       'Swaroop'   : 'swaroopch@byteofpython.info',
             'Larry'     : 'larry@wall.org',
             'Matsumoto' : 'matz@ruby-lang.org',
             'Spammer'   : 'spammer@hotmail.com',
             'zz'   : 'zhangzhao',
     }

print "Swaroop's address is %s" % ab['Swaroop']

# Adding a key/value pair
ab['Guido'] = 'guido@python.org'

print "Dict ab length is %s" % len(ab)
# Deleting a key/value pair
del ab['Spammer']
print "Dict ab length is %s" % len(ab)

print "ab['zz'] value is %s" % ab['zz']
print "After modify zz"
ab['zz'] = "zhangzhao@bstar.com.cn"
print "ab['zz'] value is %s" % ab['zz']


print '\nThere are %d contacts in the address-book\n' % len(ab)
for name, address in ab.items():
    print 'Contact %s at %s' % (name, address)

if 'Guido' in ab: # OR ab.has_key('Guido')
    print "\nGuido's address is %s" % ab['Guido']

print "After clear dict ab"
ab.clear()
print "Dict ab length is %s" % len(ab)
