"""
cloak of invisibility
using
Computer Vision OpenCV Python library
"""

import cv2 as cv
import numpy as np
import time


#create object which will be working with video file

cap = cv.VideoCapture(0)
width=int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height=int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print(width,height)

#define atribute with codec which will be saving output file

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi',fourcc, 30.0, (width,height))


#time for the camera to turn it on

time.sleep(3)
background=0

#save the first 60 frames to set base image

for i in range(60):
    ret,background = cap.read()

while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    # img = np.flip(img,axis=1)

    #Change representation of colour palette from RGB to HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #define the colour of our cap
    #prepare the mask of colours which will be represent out cloak of invisibility

    lower_colour = np.array([0,120,70])
    upper_colour = np.array([10,255,255])
    mask1 = cv.inRange(hsv,lower_colour,upper_colour)
    lower_colour = np.array([21,30,0])
    upper_colour = np.array([36,72,97])
    mask2 = cv.inRange(hsv,lower_colour,upper_colour)
    mask1 = mask1+mask2

    #operation to prepare our mask to get the invisibility effect

    mask1 = cv.morphologyEx(mask1, cv.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv.bitwise_not(mask1)

    res1 = cv.bitwise_and(background, background, mask=mask1)
    res2 = cv.bitwise_and(img, img, mask=mask2)
    final_output = cv.addWeighted(res1, 1,res2, 1, 0)

    print(type(final_output))
    out.write(final_output)
    cv.imshow('This is your finally effect', final_output)

    # use q to stop recording
    if cv.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()





