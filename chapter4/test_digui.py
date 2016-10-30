#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

def loop(self,i,subs={}):

    if i>10: return
    else :
        self.subs=subs
        self.subs[i]=i*100;
        loop(++i, self.subs)
        for sub in subs:
            print sub[0],sub[1]

loop(1,{})
