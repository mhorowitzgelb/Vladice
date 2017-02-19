import cv2 as cv
import numpy as np
from bot import RaspberryPI
import cPickle

cv.namedWindow("calibrate green",cv.WINDOW_NORMAL)
cv.namedWindow('original',cv.WINDOW_NORMAL)
cv.resizeWindow("calibrate green", 960, 540)
cv.createTrackbar('track_green_hl','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_hh','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_sl','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_sh','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_vl','calibrate green',0,255,lambda x:x)
cv.createTrackbar('track_green_vh','calibrate green',0,255,lambda x:x)

cv.namedWindow("calibrate red",cv.WINDOW_NORMAL)
cv.resizeWindow("calibrate red", 960, 540)
cv.createTrackbar('track_red_hl','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_hh','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_sl','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_sh','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_vl','calibrate red',0,255,lambda y:y)
cv.createTrackbar('track_red_vh','calibrate red',0,255,lambda y:y)

cv.namedWindow("calibrate blue",cv.WINDOW_NORMAL)
cv.resizeWindow('calibrate blue', 960, 540)
cv.createTrackbar('track_blue_hl','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue_hh','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue_sl','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue_sh','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue_vl','calibrate blue',0,255,lambda z:z)
cv.createTrackbar('track_blue_vh','calibrate blue',0,255,lambda z:z)

pi = RaspberryPI()
img = pi.take_picture()
hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('original', img)

while True:
    hl = cv.getTrackbarPos('track_green_hl','calibrate green')
    hh = cv.getTrackbarPos('track_green_hh','calibrate green')
    sl = cv.getTrackbarPos('track_green_sl','calibrate green')
    sh = cv.getTrackbarPos('track_green_sh','calibrate green')
    vl = cv.getTrackbarPos('track_green_vl','calibrate green')
    vh = cv.getTrackbarPos('track_green_vh','calibrate green')
    low_green = (hl,sl,vl)
    high_green = (hh,sh,vh)
    mask = cv.inRange(hsv_img,low_green,high_green)
    cv.imshow('calibrate green', mask)
    if(cv.waitKey(100)== 10):
        break

cv.destroyWindow("calibrate green")

bound_dict = {'green' : (low_green,high_green)}

cv.imshow('original', img)

while True:
    hl = cv.getTrackbarPos('track_red_hl','calibrate red')
    hh = cv.getTrackbarPos('track_red_hh','calibrate red')
    sl = cv.getTrackbarPos('track_red_sl','calibrate red')
    sh = cv.getTrackbarPos('track_red_sh','calibrate red')
    vl = cv.getTrackbarPos('track_red_vl','calibrate red')
    vh = cv.getTrackbarPos('track_red_vh','calibrate red')
    low_red = (hl,sl,vl)
    high_red = (hh,sh,vh)
    mask = cv.inRange(hsv_img,low_red,high_red)
    cv.imshow('calibrate red', mask)
    if(cv.waitKey(100)== 10):
        break

cv.destroyWindow('calibrate red')

bound_dict['red'] = (low_red,high_red)

cv.destroyAllWindows()

cv.imshow('original', img)


while True:
    hl = cv.getTrackbarPos('track_blue_hl','calibrate blue')
    hh = cv.getTrackbarPos('track_blue_hh','calibrate blue')
    sl = cv.getTrackbarPos('track_blue_sl','calibrate blue')
    sh = cv.getTrackbarPos('track_blue_sh','calibrate blue')
    vl = cv.getTrackbarPos('track_blue_vl','calibrate blue')
    vh = cv.getTrackbarPos('track_blue_vh','calibrate blue')
    low_blue = (hl,sl,vl)
    high_blue = (hh,sh,vh)
    mask = cv.inRange(hsv_img,low_blue,high_blue)
    cv.imshow('calibrate blue', mask)
    if(cv.waitKey(100)== 10):
        break

cv.destroyWindow('calibrate blue')

bound_dict['blue'] = (low_blue,high_blue)

f = open('bounds.pkl','wb')
cPickle.dump(bound_dict,f,cPickle.HIGHEST_PROTOCOL)

cv.destroyAllWindows()
