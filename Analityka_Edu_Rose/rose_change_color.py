import cv2 as cv
import os
import numpy as np

file_path = os.path.dirname(__file__)

img = cv.imread(file_path+'/rose.jpg')

hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

h,s,v = cv.split(hsv)

#cv.imshow('hue',h)
#cv.imshow('saturation',s)
#cv.imshow('value',v)


#create mask



#because we have got trash on the left side, we must prepare one more mask and merge them
lower_red = np.array([0,165,50])
upper_red = np.array([10,255,255])
mask0 = cv.inRange(hsv, lower_red, upper_red)
cv.imshow('lower',mask0)

lower_red = np.array([170,165,50])
upper_red = np.array([179,255,255])

mask1 = cv.inRange(hsv, lower_red, upper_red)
cv.imshow('upper',mask1)

mask = mask0 + mask1
cv.imshow('merged',mask)

#cv.imshow('mask',mask)



#prepare image in gray scale

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#prepare gray scale image to rgb

img_gray_rgb = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
mask = cv.bitwise_not(mask)
img_gray_rgb = cv.bitwise_not(img_gray_rgb)


#solution - display image in gray scale with red rose

rose = cv.bitwise_not(img_gray_rgb,img,mask=mask)
cv.imshow('rose',rose)



cv.waitKey(0)
cv.destroyAllWindows()