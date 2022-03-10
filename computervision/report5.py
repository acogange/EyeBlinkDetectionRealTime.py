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
print(y_hist1)
out = (np.dstack((y_hist1,cr,cb))).astype(np.uint8)  #고친 y값과 Cr Cb 모아서
ycctorgb=cv2.cvtColor(out, cv2.COLOR_YCrCb2BGR) #YCrCb-> RGB

func_pnsr=cv2.PSNR(resize_img,ycctorgb)
print("함수 PSNR",func_pnsr)
cv2.imshow('ori',resize_img)
cv2.imshow('func_his',ycctorgb)

#수식 사용


r, c = resize_img.shape[:2]

p_max = max(map(max, y))

unique, counts = np.unique(y, return_counts=True)
count_dic = (dict(zip(unique, counts)))

cnt = 0
y_hist2 = []
# 빈도수 표 만들기
for key, value in count_dic.items():  # 밝기값(brightness) , 밝기값의 빈도수(number) 표 만들기
    cnt += value  # sum 누적 빈도
    his = (math.floor(((p_max + 1) / (r * c)) * cnt - 1))  # 히스토그램 수식 변환  method_1   올림(normalized)
    y_hist2.append(his)  # 변환한 값(int1)

his_dic = (dict(zip(unique, y_hist2)))  # 밝기(기준), int 1(적용값) dictionary 만들기

for key, value in his_dic.items():
    for i in range(r):
        for j in range(c):
            if y[i][j] == key:  # 픽셀의 밝기에 따른
                y[i][j] = value  # 값 설정

out2 = (np.dstack((y, cr, cb))).astype(np.uint8)  # 고친 y값과 Cr Cb 모아서
ycctorgb2 = cv2.cvtColor(out2, cv2.COLOR_YCrCb2BGR)  # YCrCb-> RGB

func_pnsr2 = cv2.PSNR(resize_img, ycctorgb2)

print("수식 PSNR:", func_pnsr2)
cv2.imshow('his2', ycctorgb2)
cv2.waitKey(0)

