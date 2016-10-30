#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

import searchengine

craw=searchengine.crawler('searchindex.db')
# craw.createindextables()
pages=[
  # 'http://www.bbc.com/',
  'https://www.hao123.com/?1477704964',
  # 'https://www.baidu.com',
]

# craw.crawl(pages)

e=searchengine.searcher('searchindex.db')
print e.getmatchrows('hao weather yes')
