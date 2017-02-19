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
cv.createTrackbar('track_red_hl','calibrate red',0,510,lambda y:y)
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

f = open("bounds.pkl",'rb')
bounds = cPickle.load(f)

red_bounds = bounds['red']
blue_bounds = bounds['blue']
green_bounds = bounds['green']

red_hl = red_bounds[0][0]
red_hh = red_bounds[1][0]
red_sl = red_bounds[0][1]
red_sh = red_bounds[1][1]
red_vl = red_bounds[0][2]
red_vh = red_bounds[1][2]


blue_hl = blue_bounds[0][0]
blue_hh = blue_bounds[1][0]
blue_sl = blue_bounds[0][1]
blue_sh = blue_bounds[1][1]
blue_vl = blue_bounds[0][2]
blue_vh = blue_bounds[1][2]

green_hl = green_bounds[0][0]
green_hh = green_bounds[1][0]
green_sl = green_bounds[0][1]
green_sh = green_bounds[1][1]
green_vl = green_bounds[0][2]
green_vh = green_bounds[1][2]

cv.setTrackbarPos('track_green_hl','calibrate green',green_hl)
cv.setTrackbarPos('track_green_hh','calibrate green',green_hh)
cv.setTrackbarPos('track_green_sl','calibrate green',green_sl)
cv.setTrackbarPos('track_green_sh','calibrate green',green_sh)
cv.setTrackbarPos('track_green_vl','calibrate green',green_vl)
cv.setTrackbarPos('track_green_vh','calibrate green',green_vh)

cv.setTrackbarPos('track_red_hl','calibrate red',red_hl)
cv.setTrackbarPos('track_red_hh','calibrate red',red_hh)
cv.setTrackbarPos('track_red_sl','calibrate red',red_sl)
cv.setTrackbarPos('track_red_sh','calibrate red',red_sh)
cv.setTrackbarPos('track_red_vl','calibrate red',red_vl)
cv.setTrackbarPos('track_red_vh','calibrate red',red_vh)

cv.setTrackbarPos('track_blue_hl','calibrate blue',blue_hl)
cv.setTrackbarPos('track_blue_hh','calibrate blue',blue_hh)
cv.setTrackbarPos('track_blue_sl','calibrate blue',blue_sl)
cv.setTrackbarPos('track_blue_sh','calibrate blue',blue_sh)
cv.setTrackbarPos('track_blue_vl','calibrate blue',blue_vl)
cv.setTrackbarPos('track_blue_vh','calibrate blue',blue_vh)




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
    hl = cv.getTrackbarPos('track_red_hl','calibrate red') - 255
    hh = cv.getTrackbarPos('track_red_hh','calibrate red')
    sl = cv.getTrackbarPos('track_red_sl','calibrate red')
    sh = cv.getTrackbarPos('track_red_sh','calibrate red')
    vl = cv.getTrackbarPos('track_red_vl','calibrate red')
    vh = cv.getTrackbarPos('track_red_vh','calibrate red')
    low_red = (hl,sl,vl)
    high_red = (hh,sh,vh)

    if hl < 0:
        mask = cv.bitwise_or(cv.inRange(hsv_img, (255 + hl, sl, vl), (255, sh, vh)),
                             cv.inRange(hsv_img,(0, sl, vl), (hh, sl, vl)))
    else:
        mask = cv.inRange(hsv_img,low_red,high_red)
    cv.imshow('calibrate red', mask)
    if(cv.waitKey(100)== 10):
        break

cv.destroyWindow('calibrate red')

bound_dict['red'] = (low_red,high_red)


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
