import cv2 as cv
import numpy as np
from bot import RaspberryPI

cv.namedWindow("calibrate green",cv.WINDOW_NORMAL)
cv.namedWindow('original',cv.WINDOW_NORMAL)
cv.resizeWindow("calibrate green", 960, 540)
cv.createTrackbar('track_green_hl','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_hh','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_sl','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_sh','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_vl','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_vh','calibrate green',0,255,lambda x:x)
'''
cv.namedWindow("calibrate red")
cv.resizeWindow("calibrate red", 960, 540)
cv.createTrackbar('track_red_hl','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_hh','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_sl','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_sh','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_vl','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_vh','calibrate red',0,255,lambda y:y)

cv.namedWindow("calibrate blue")
cv.resizeWindow('calibrate blue', 960, 540)
cv.createTrackbar('track_blue','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue','calibrate blue',0,255,lambda z:z)
'''
pi = RaspberryPI()
img = pi.take_picture()
hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

while True:
    hl = cv.getTrackbarPos('track_green_hl','calibrate green')
    hh = cv.getTrackbarPos('track_green_hh','calibrate green')
    sl = cv.getTrackbarPos('track_green_sl','calibrate green')
    sh = cv.getTrackbarPos('track_green_sh','calibrate green')
    vl = cv.getTrackbarPos('track_green_vl','calibrate green')
    vh = cv.getTrackbarPos('track_green_vh','calibrate green')
    low = (hl,sl,vl)
    high = (hh,sh,vh)
    mask = cv.inRange(hsv_img,low,high)
    cv.imshow('original',img)
    cv.imshow('calibrate green', mask)
    if(cv.waitKey(10)== 27):
        break

cv.destroyAllWindows()

