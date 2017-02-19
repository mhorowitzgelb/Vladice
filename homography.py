#!/usr/bin/env python

import cv2
import numpy as np
from circle_detection import get_square_points
import cPickle


scale  = 50
def run_homography(im_src):
    cv2.namedWindow("srcImage")

    (h,w,z) = im_src.shape

    #im_src = cv2.resize(im_src,(w/2,h/2))


    #cv2.setMouseCallback("srcImage", click_corners)


    # Read source image.

    points_unsorted = get_square_points(im_src)

    left_aboves = np.zeros((4,2))

    for i in range(4):
        for j in range(i+1,4):
            point_i = points_unsorted[i][0]
            point_j = points_unsorted[j][0]
            if point_i[0] < point_j[0]:
                left_aboves[i][0] += 1
            else:
                left_aboves[j][0] += 1
            if point_i[1] < point_j[1]:
                left_aboves[i][1] += 1
            else:
                left_aboves[j][1] += 1

    pts_src = np.zeros((4,2),dtype=np.int)


    for i in range(4):
        left_above = left_aboves[i]
        if left_above[0] >=2 and left_above[1] >= 2:
            pts_src[0,0] = points_unsorted[i][0][0]
            pts_src[0,1] = points_unsorted[i][0][1]
        elif left_above[0] < 2 and left_above[1] >= 2:
            pts_src[1, 0] = points_unsorted[i][0][0]
            pts_src[1, 1] = points_unsorted[i][0][1]
        elif left_above[0] <2 and left_above[1] < 2:
            pts_src[2, 0] = points_unsorted[i][0][0]
            pts_src[2, 1] = points_unsorted[i][0][1]
        elif left_above[0] >= 2 and left_above[1] < 2:
            pts_src[3, 0] = points_unsorted[i][0][0]
            pts_src[3, 1] = points_unsorted[i][0][1]



    #for pt in pts_src:
     #   cv2.circle(im_src,(pt[0],pt[1]),20,(0,0,255),thickness=4)

    cv2.imshow("srcImage", im_src)




    pts_dst = np.array([[0, 0], [11*scale -1, 0], [11*scale -1, 11* scale -1], [0, 11* scale -1]])



    # Calculate Homography
    h, status = cv2.findHomography(np.array(pts_src), pts_dst)

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (11*scale, 11*scale))

    # Display images
    #cv2.imshow("Warped Source Image", im_out)

    #gray_scale = cv2.cvtColor(im_out,cv2.COLOR_BGR2GRAY)

    #cv2.namedWindow("edge_detection")



    #cv2.createTrackbar("Threshold", 'edge_detection', 0,255, lambda x: x)





    for i in range(1, 11):
        cv2.line(im_out,(i * scale, 0), (i* scale, 11* scale -1),(0,255,0),scale / 5)
        cv2.line(im_out,(0, i * scale), (11* scale-1, i*scale),(0,255,0),scale / 5)

    board_array = get_board_array(im_out)

    #test_red = cv2.cvtColor(im_out,cv2.COLOR_BGR2HSV)
    #test_red = cv2.inRange(test_red,lower_red,upper_red)
    #cv2.imshow("red-thresh",test_red)
    #print("red thresh ",len(np.nonzero(test_red)[0]))

    for i in range(11):
        for j in range(11):
            if(board_array[i,j] == 2):
                cv2.circle(im_out,(j* scale + scale/2, i*scale + scale/2),scale/2 - 5,(0,0,255),10)
            elif(board_array[i,j] == 1):
                cv2.circle(im_out, (j * scale + scale / 2, i * scale + scale / 2), scale / 2 - 5, (255, 0, 0), 10)




    cv2.imshow("lines", im_out)



    cv2.waitKey(3000)

    ##cv2.destroyAllWindows()
    return board_array


def click_corners(event, x, y, flags, param):
    # grab references to the global variables
    global pts_src, points_selected
    if points_selected:
        return




    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Got point", x, ", ", y)
        pts_src.append([x, y])
        if (len(pts_src) == 4):
            points_selected = True


f = open('bound_working.pkl','rb')
bound = cPickle.load(f)

red_bound = bound['red']
blue_bound = bound['blue']

lower_red = red_bound[0]
upper_red = red_bound[1]

lower_blue = blue_bound[0]
upper_blue = blue_bound[1]

def get_piece(square):
    hsv_square = cv2.cvtColor(square,cv2.COLOR_BGR2HSV)
    hl = lower_red[0]
    sl = lower_red[1]
    vl = lower_red[2]
    hh = upper_red[0]
    sh = upper_red[1]
    vh = upper_red[2]
    if hl < 0:
        red_mask = cv2.bitwise_or(cv2.inRange(hsv_square, (255 + hl, sl, vl), (255, sh, vh)),
                             cv2.inRange(hsv_square, (0, sl, vl), (hh, sl, vl)))
    else:
        red_mask = cv2.inRange(hsv_square,lower_red,upper_red)

    blue_mask = cv2.inRange(hsv_square,lower_blue,upper_blue)
    nonzero_blue = np.nonzero(blue_mask)
    nonzero_red = np.nonzero(red_mask)
    red_ratio = (float(len(nonzero_red[0])) / (red_mask.shape[0] *red_mask.shape[1]))
    blue_ratio = (float(len(nonzero_blue[0]))/(blue_mask.shape[0]* blue_mask.shape[1]))
    if(red_ratio < 0.3 and blue_ratio <0.3):
        return 0
    elif red_ratio > blue_ratio:
        return 2
    else:
        return 1



def get_board_array(squared_img):
    board = np.zeros((11,11),dtype=np.int)
    for i  in range(11):
        for j in range(11):
            square = squared_img[i*scale:(i+1)*scale,j*scale:((j+1)*scale),:]
            board[i,j] = get_piece(square)
    return board



if __name__ == '__main__':
    img = cv2.imread("board_small.jpg")
    run_homography(img)
