"""Color detection"""
import cv2 as cv
import numpy as np
import os

file_path = os.path.dirname(__file__)

#stack fnc

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


#create an empty function for trackbar
def empty(a):
    pass

#create new window -
cv.namedWindow('Track Bars')
cv.resizeWindow('Track Bars',640,240) #the name must be the same like above, and we choose size
cv.createTrackbar('Hue min','Track Bars',150,179,empty) #in opencv maximum hue is 179 not 360
cv.createTrackbar('Hue max','Track Bars',179,179,empty)
cv.createTrackbar('Sat min','Track Bars',30,255,empty)
cv.createTrackbar('Sat max','Track Bars',255,255,empty)
cv.createTrackbar('Val min','Track Bars',22,255,empty)
cv.createTrackbar('Val max','Track Bars',255,255,empty)

cap = cv.VideoCapture(0)


#put everything in while loop to automatic changing HSV values
while True:
    success, img = cap.read()
    #create images
    imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    #get trackbar position from createTrackbar fnc


    h_min = cv.getTrackbarPos('Hue min','Track Bars')
    h_max = cv.getTrackbarPos('Hue max','Track Bars')
    s_min = cv.getTrackbarPos('Sat min','Track Bars')
    s_max = cv.getTrackbarPos('Sat max','Track Bars')
    v_min = cv.getTrackbarPos('Hue min','Track Bars')
    v_max = cv.getTrackbarPos('Val max','Track Bars')

    #create mask for HSV image , the white colour is what we need, but the black is that we don't

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])

    mask = cv.inRange(imgHSV,lower,upper)

    result = cv.bitwise_and(img,img,mask=mask)


    #stack images
    stackedImg = stackImages(0.5,([img,mask,result]))
    cv.imshow('Stacked Images',stackedImg)

    #close window
    if cv.waitKey(10) & 0xFF == ord('q'):
        break