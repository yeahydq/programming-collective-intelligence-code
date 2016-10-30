#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

#encoding=utf-8
import jieba
from jieba import posseg

seg_list = jieba.cut("我来到北京清华大学",cut_all=True)
print "Full Mode:", "/ ".join(seg_list) #全模式

seg_list = jieba.cut("我来到北京清华大学",cut_all=False)
print "Default Mode:", "/ ".join(seg_list) #精确模式

seg_list = jieba.cut("他来到了网易杭研大厦") #默认是精确模式
print ", ".join(seg_list)

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") #搜索引擎模式
print ", ".join(seg_list)

seg_list  = jieba.cut_for_search("Xiaoming was gradued in the Chinese SCAU, after that, he keep study in the Janpan") #搜索引擎模式
print ", ".join(seg_list)

seg_list = posseg.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") #词性
print [(w.word.encode('gbk'),w.flag) for w in seg_list]
# for w in seg_list:
#     print w.word,w.flag

# print [w.word,w.flag   for w in seg_list]

