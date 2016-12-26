#coding:utf-8
#!/usr/bin/env python
__author__ = 'dick'

# from pytesser import *
# print image_file_to_string('./1.jpg')
# # print image_file_to_string('/dick/test/1.jpg')

from pytesser import *
image = Image.open('1.bmp')  # Open image object using PIL
print image_to_string(image)


