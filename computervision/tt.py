#21812223 김효정
import cv2
import numpy as np
import collections
import math
imgfile='aaa.png'
img=cv2.imread(imgfile, cv2.IMREAD_COLOR)
resize_img = cv2.resize(img, (300, 300))
rgbtoycc=cv2.cvtColor(resize_img, cv2.COLOR_BGR2YCrCb) #함수 사용 RGB->YCbCr

#함수 사용
y, cr, cb = cv2.split(rgbtoycc)  #y값만 histogram하려고 각 배열 분리

y_hist1=cv2.equalizeHist(y)  #y만 histogram
out = (np.dstack((y_hist1,cr,cb))).astype(np.uint8)  #고친 y값과 Cr Cb 모아서
ycctorgb=cv2.cvtColor(out, cv2.COLOR_YCrCb2BGR) #YCrCb-> RGB





r, c = resize_img.shape[:2]






out2 = (np.dstack((y, cr, cb))).astype(np.uint8)  # 고친 y값과 Cr Cb 모아서
ycctorgb2 = cv2.cvtColor(out2, cv2.COLOR_YCrCb2BGR)  # YCrCb-> RGB

func_pnsr2 = cv2.PSNR(resize_img, ycctorgb2)


cv2.imshow('his2', ycctorgb2)
cv2.waitKey(0)

