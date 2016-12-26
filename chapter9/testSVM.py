#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

# http://blog.csdn.net/zy825316/article/details/18989451
# http://www.cnblogs.com/lifegoesonitself/archive/2013/08/01/3230264.html
from svm import *
from svmutil import *

# from svm import LINEAR
prob=svm_problem([1,-1],[[1,0,1],[-1,0,-1]])

param = svm_parameter()#与书中不同，这是新版本的改进，用下面的方法来指定使用的核方法
param.kernel_type = LINEAR#跟多内容参见博客
param.C = 10
model = svm_train(prob, param)#训练
print svm_predict([1],[[1,1,1]],model)#第一个参数我是自己预测的，第二个参数是需要判断的数据，第三个就是训练模型

#
# array="-t 0 -c 10"
# param=svm_parameter(array)
# m=svm_model(prob,param)

#
# from svmutil import *
#  y,x = svm_read_problem('../heart_scale')
#  m = svm_train(y[:200], x[:200], '-c 4')
#  p_label, p_acc, p_val = svm_predict(y[200:],x[200:],m)
#
#
