import cv2
import numpy as np
from matplotlib import pyplot as plt

imgfile = 'b.png'
img = cv2.imread(imgfile, cv2.IMREAD_COLOR) # 원본
cv2.imshow('original image',img)

img_R2YC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB) # RGB -> YCbCr
y, cr, cb = cv2.split(img_R2YC)

edges = cv2.Canny(y, 100, 200) # 임계값 각각 100과 200
lines = cv2.HoughLines(edges, 1, np.pi/180, 100) #100개의 점을 1개의 선으로

for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)

cv2.imshow('cany Edge Detection', edges) #edge 검출
cv2.imshow('ori + houghLines', img)

cv2.waitKey()