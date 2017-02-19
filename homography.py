#!/usr/bin/env python

import cv2
import numpy as np
from circle_detection import get_square_points




scale  = 50
def run_homography(im_src):
    cv2.namedWindow("srcImage")

    (h,w,z) = im_src.shape

    im_src = cv2.resize(im_src,(h/2,w/2))


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



    for pt in pts_src:
        cv2.circle(im_src,(pt[0],pt[1]),20,(0,0,255),thickness=4)

    cv2.imshow("srcImage", im_src)




    pts_dst = np.array([[0, 0], [11*scale -1, 0], [11*scale -1, 11* scale -1], [0, 11* scale -1]])



    # Calculate Homography
    h, status = cv2.findHomography(np.array(pts_src), pts_dst)

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (11*scale, 11*scale))

    # Display images
    cv2.imshow("Warped Source Image", im_out)

    gray_scale = cv2.cvtColor(im_out,cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("edge_detection")



    cv2.createTrackbar("Threshold", 'edge_detection', 0,255, lambda x: x)


    while(1):
        thresh = cv2.getTrackbarPos("Threshold","edge_detection")
        mask = ((gray_scale <=thresh) * 255).astype(np.uint8)
        #print(mask)
        cv2.imshow("edge_detection", mask )
        if cv2.waitKey(10) == 27:
            break

    for i in range(1, 11):
        cv2.line(im_out,(i * scale, 0), (i* scale, 11* scale -1),(0,255,0),scale / 5)
        cv2.line(im_out,(0, i * scale), (11* scale-1, i*scale),(0,255,0),scale / 5)

    cv2.imshow("lines", im_out)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


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


if __name__ == '__main__':
    img = cv2.imread("board_small.jpg")
    run_homography(img)