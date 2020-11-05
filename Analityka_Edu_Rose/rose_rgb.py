import cv2 as cv
import os

file_path = os.path.dirname(__file__)

img = cv.imread(file_path+'/rose.jpg')

b,g,r = cv.split(img)
cv.imshow('blue',b)
cv.imshow('green',g)
cv.imshow('red',r)
img_merge = cv.merge((b,g,r))
cv.imshow('merged',img_merge)

cv.waitKey(0)
cv.destroyAllWindows()