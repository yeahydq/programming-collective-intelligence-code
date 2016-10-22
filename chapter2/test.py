#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'
import pydelicious
from pydelicious import *
from deliciousrec import *

# a = pydelicious.apiNew('yeahydq', '87267526')
# # a = DeliciousAPI('yeahydq', '87267526')
# a.tags_get()  # Same as:
# a.request('tags/get', )
# print a

delusers=initializeUserDict('programming')
fillItems(delusers)
print delusers.values()