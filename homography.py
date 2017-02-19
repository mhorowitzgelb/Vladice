#!/usr/bin/env python

import cv2
import numpy as np


pts_src = []
points_selected = False

scale  = 50
def main():
    cv2.namedWindow("srcImage")
    cv2.setMouseCallback("srcImage", click_corners)


    # Read source image.
    im_src = cv2.imread('board_small.jpg')
    cv2.imshow("srcImage", im_src)



    pts_dst = np.array([[0, 0], [11*scale -1, 0], [11*scale -1, 11* scale -1], [0, 11* scale -1]])
    while True:
        cv2.waitKey()
        if points_selected:
            break


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
    main()