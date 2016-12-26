#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

def printXY(x="1", y="2"):
    'print x*10+y'

    return x*10+y

# printXY()
n=3
realdist = [
            [printXY(i, j) for j in range(5)]
            for i in range(0, 3)
            ]
print realdist

print printXY(1,3)
print printXY.__doc__


def gen():
    print 'enter'
    yield 1
    print 'next'
    return
    print 'next 2'
    yield 2
    print 'next 3'


for i in gen():
    print i
