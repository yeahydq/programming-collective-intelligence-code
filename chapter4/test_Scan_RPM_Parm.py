#coding:utf-8
#!/usr/bin/env python
import re

__author__ = 'dick'



def replaceStr(str,subs={}):
    v=re.split('[\^]',str)[1]
    return str.replace('^'+v+'^',subs[v])

#
# def replaceStr(str,filename):
#     v=re.split('[\^]',str)[1]
#     for subs in getSubs(filename):
#         if v==subs[0]:
#             return str.replace('^'+v+'^',subs[1])

def getInputNew(filename='/dev/null',subs={}):
    inFiles=[]
    outFiles=[]
    subs=getSubs(filename,subs)
    input_file = open(filename,'r').read()
    for key, value in subs.items():
        input_file = input_file.replace('^'+key+'^', value);

    line=input_file.split('\n')

    for i in range(0,len(line)):
        # if remark or without '=', then next
        if (not re.match(r'.*=.*',line[i]) or
                re.match(r'#.*',line[i]) or
                re.match(r'%DISP.*',line[i])
            ) : continue

        values = re.split('[ %=]', line[i])
        type=values[1]
        jobDesc=values[2]
        value=values[3]

        if (re.match(r'PARM',type) and re.match(r'.*\.txt',value)):
            newInFiles,newOutFIles=getInputNew(value,subs)
            inFiles+=newInFiles
            outFiles+=newOutFIles
        elif (re.match(r'DS_PATH', type)):
            if (re.match(r'.*_In_.*',jobDesc)):
                # Input
                if (value not in outFiles + inFiles):
                    inFiles.append(value)
            elif (re.match(r'.*_Out_.*', jobDesc)):
                # Output
                if (value not in outFiles):
                    outFiles.append(value)
        else :
            continue


    return inFiles,outFiles

def getInput(filename='/dev/null',inFiles={},outFiles={}):
    f = open(filename,'r').read()
    s = f.split('\n')
    for i in range(0,len(s)):
        if not re.match(r'.*=.*',s[i]): continue
        values = re.split('[ %=]', s[i])
        jobDesc = values[2]
        ioName = replaceStr(values[3], getSubs(filename))
        m = re.match(r'%PARM%.*Seq.*txt', jobDesc)
        if m : inFiles,outFiles = getInput(m.group(),inFiles,outFiles)

        m = re.match(r'%DS_PATH%.*', s[i])
        if m :
            str=m.group()+s[i+1]
            values=re.split('[ %=]',str)
            jobDesc=values[2]
            ioName=replaceStr(values[3],filename)
            keepDel=values[5]
            if re.match(r'.*_In_.*',jobDesc):
                ioType="I"
                if (ioName not in outFiles + inFiles):
                    inFiles.append(ioName)
            else :
                ioType='O'
                if (ioName not in outFiles):
                    outFiles.append(ioName)
            # print [type,ioName,keepDel]
    return inFiles,outFiles

def getSubs(filename='/dev/null',parentSubs={}):
    f = open(filename,'r').read()
    s = f.split('\n')
    subs=parentSubs
    for i in range(0,len(s)):
        m = re.match(r'%SUB%.*', s[i])
        if m :
            # n = m.group().split('=')
            n=re.split('[%=]',m.group())
            subs[n[2]]=n[3]
    return subs

file_1='Parm_Seq_013.txt'
file_2='Parm_Seq_014.txt'

# print replaceStr('^DS_File_Path^rpm_cust_s013_j001.ds',filename)

inFiles = []
outFiles = []
getInputNew(file_1)
#
# inFiles,outFiles=getInput(file_1,inFiles,outFiles)
# inFiles,outFiles=getInput(file_2,inFiles,outFiles)
# for file in inFiles:
#     print "Input is : ",file
#
# for file in outFiles:
#     print "Output is : ",file
#
# # for i,value in getSubs(filename):
# #     print i,"value is:",value
