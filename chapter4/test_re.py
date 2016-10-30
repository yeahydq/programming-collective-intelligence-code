#coding:utf-8
#!/usr/bin/env python
import re

__author__ = 'dick'

url='www.hao123.com'
url='hello'
pattern = re.compile(r'hao123')
match = pattern.match("hello word")
if match:
    print url
else:
    print("unmatch=%s"%url)

pi=3.1415926
print( "pi = %.*f" % ( 3,pi))


m = re.match(r'hello', 'hello world!')
print m.group()

m = re.match(r'.*hao123\.com', 'www.hao123.com')
print m.group()

m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
