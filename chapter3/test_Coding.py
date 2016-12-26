# coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

# -*- coding=UTF-8 -*-
if __name__ == '__main__':
    utf8 = '中国'
    unic = u'中国'
    #s为unicode先转为utf-8
    #因为s为所在的.py(# -*- coding=UTF-8 -*-)编码为utf-8
    print type(utf8),len(utf8),utf8

    newUTF8=unic.encode('utf-8')
    print type(newUTF8),len(newUTF8),newUTF8

    newUnic=utf8.decode('utf-8')
    print type(newUnic),len(newUnic),newUnic

    newGBK=utf8.decode('utf-8').encode('gbk')
    print type(newGBK),len(newGBK),newGBK

    # utf8=s.decode('UTF-8')
    # print
    # #s转为gb2312:先转为unicode再转为gb2312
    # print s.decode('utf-8').encode('gb2312')
