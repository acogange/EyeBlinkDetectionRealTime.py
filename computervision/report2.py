import cv2
import numpy as np
imgfile='comhh.png'

img=cv2.imread(imgfile, cv2.IMREAD_COLOR)

#함수 이용 변환
rgbtoycc=cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
ycctorgb=cv2.cvtColor(rgbtoycc, cv2.COLOR_YCrCb2BGR)

y2, cr2, cb2 = cv2.split(rgbtoycc)

cv2.imshow('img',img)
cv2.imshow('f_out1',y2)
cv2.imshow('f_out2',ycctorgb)

#수식 이용 변환

img2 = cv2.imread('comhh.png')
height, width, channel = img.shape
r = img[..., 0]
g = img[..., 1]
b = img[..., 2]

y = np.zeros((height, width), dtype=np.float)
cr = np.zeros((height, width), dtype=np.float)
cb = np.zeros((height, width), dtype=np.float)
#ycc변환
for i in range(height):
    for j in range(width):
        y[i][j] = 0.299 * r[i][j] + 0.587 * g[i][j] + 0.114 * b[i][j]
        cb[i][j] = 128 - 0.172 * r[i][j] - 0.339 * g[i][j] + 0.511 * b[i][j]
        cr[i][j] = 128 + 0.511 * r[i][j] - 0.428 * g[i][j] - 0.083 * b[i][j]

out = (np.dstack((y, cr, cb))).astype(np.uint8)#변환한 값 합치고
y2, cr2, cb2 = cv2.split(out)#각 요소 분리해서 값 저장
cv2.imshow('out1',y2)#밝기 부분만 이미지로 출력
#rgb복원시킬 리스트 정의
R = np.zeros((height, width), dtype=np.float)
G = np.zeros((height, width), dtype=np.float)
B = np.zeros((height, width), dtype=np.float)
#rgb변환
for i in range(height):
    for j in range(width):
        R[i][j] = y[i][j] +( 1.371* (cr[i][j] - 128))
        G[i][j] = y[i][j] -( 0.336 * (cb[i][j] - 128) )- (0.698 * (cr[i][j] - 128))
        B[i][j] = y[i][j] + (1.732 * (cb[i][j] - 128))

out2 = (np.dstack((R, G, B))).astype(np.uint8)

cv2.imshow('out2',out2)
cv2.waitKey(0)