import cv2
import math
import numpy as np
from skimage.metrics import *
imgfile='comhh.png'

img=cv2.imread(imgfile, cv2.IMREAD_COLOR)
r,g,b= cv2.split(img)
#함수 이용 변환
rgbtoycc=cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
img2=cv2.cvtColor(rgbtoycc, cv2.COLOR_YCrCb2BGR)
r2, g2, b2 = cv2.split(img2)
#func_pnsr=peak_signal_noise_ratio(img,img2)

func_pnsr=cv2.PSNR(img,img2)

def psnr(ori_img,make_img):
    # 원본과 복원 파일 각 rgb 원소 차이
    mse_r = np.mean((r - r2) ** 2)
    mse_g = np.mean((g - g2) ** 2)
    mse_b = np.mean((b - b2) ** 2)

    mse_t=mse_r+mse_b+mse_g #각 필터의 mse합
    if mse_t ==0: #오차가 없으면
        return 100  #품질이 좋은 PSNR
    else:
        return 10*math.log10((255**2)/mse_t)

make_psnr=psnr(img,img2)
print("함수 사용 PSNR",func_pnsr)
print("계산한 PSNR",make_psnr)

print("오차",func_pnsr-make_psnr)