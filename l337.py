intab = 'aeio'
outtab = '4310'
s = input ('Enter your password:')
print(s.translate({ord(x): y for (x, y) in zip(intab, outtab)}))
