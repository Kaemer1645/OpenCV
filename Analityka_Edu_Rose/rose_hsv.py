import cv2 as cv
import os
import numpy as np

file_path = os.path.dirname(__file__)

img = cv.imread(file_path+'/rose.jpg')

hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

h,s,v = cv.split(hsv)
cv.imshow('hue',h)
cv.imshow('saturation',s)
cv.imshow('value',v)
img_merge = cv.merge((h,s,v))
output_merged = cv.cvtColor(img_merge,cv.COLOR_HSV2BGR)
cv.imshow('merged',output_merged)

cv.waitKey(0)
cv.destroyAllWindows()