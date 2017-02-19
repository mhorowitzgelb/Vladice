import cv2 as cv
import numpy as np



def get_square_points(image):

    #cv.imshow("original", image)

    hsv_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)

    #cv.setMouseCallback("original",click_color)

    greenLower = (29, 150, 50)
    greenUpper = (70, 255, 255)

    mask = cv.inRange(hsv_image, greenLower, greenUpper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    #cv.imshow("mask", mask)
    iter_mask = mask.copy()
    cv.imshow("color_mask", mask)

    points = []
    nonzero = np.nonzero(mask)

    h, w = iter_mask.shape[:2]

    flood_mask = np.zeros((h+2,w+2), dtype=np.uint8)
    i = 0
    while(len(nonzero[0]) > 0):
        i += 1
        print("circle", i)
        first_point = (nonzero[1][0],nonzero[0][0])
        fill = iter_mask.copy()
        cv.floodFill(fill,flood_mask,first_point,0)
        single_circle =  iter_mask - fill
        M = cv.moments(single_circle)
        if not M["m00"] == 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            points.append(((cX,cY),np.sum(single_circle)))
        iter_mask = iter_mask - single_circle
        nonzero = np.nonzero(iter_mask)
        #cv.imshow("current iter_mask", iter_mask)

    top_four_points = []

    for point in points:
        if len(top_four_points) < 4:
            top_four_points.append(point)

        else:
            for i in range(4):
                other = top_four_points[i]
                if(point[1] > other[1]):
                    top_four_points[i] = point
                    break


    for point in top_four_points:
        print(point)
        cv.circle(mask,point[0],20,255)



    #cv.imshow("points",mask)
    #cv.waitKey(0)
    return top_four_points



