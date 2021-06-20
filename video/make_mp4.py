# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : make_mp4.py
# Time       ：2021/6/20 23:16
# version    ：python 3.7
# Description：
"""

import cv2

img = cv2.imread('tempAA.png')  # 读取第一张图片
imgInfo = img.shape
size = (imgInfo[1], imgInfo[0])  # 获取图片宽高度信息
print(size)

videoWrite = cv2.VideoWriter('2.mp4', -1, 5, size)  # 根据图片的大小，创建写入对象 （文件名，支持的编码器，5帧，视频大小（图片大小））

for i in range(1, 3):
    fileName = 'temp0' + str(i) + '.gif'  # 循环读取所有的图片
    img = cv2.imread(fileName)

    videoWrite.write(img)  # 将图片写入所创建的视频对象

print('end!')
