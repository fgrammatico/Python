#!/usr/bin/env python3

intab = 'qwertyuiopasdfghjklzxcvbnm'
outtab = 'qw3r7yu10p45df6hjklzxcvbnm'
s = input ('Enter your password:')
print(s.translate({ord(x): y for (x, y) in zip(intab, outtab)}))
