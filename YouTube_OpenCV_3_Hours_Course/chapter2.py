"""Work with blurring, edges detection, """
import cv2 as cv
import os
import numpy as np

file_path = os.path.dirname(__file__)


#read img

img = cv.imread(file_path+'/snake.jpg')
kernel = np.ones((5,5),np.uint8)

#img from RGB to grayscale

imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
imgBlur = cv.GaussianBlur(img, (11,11),0)
imgCanny = cv.Canny(img,100,100)
imgDialation = cv.dilate(imgCanny,kernel,iterations=1)
imgEroded = cv.erode(imgDialation,kernel,iterations=1)

cv.imshow('Gray',imgGray)
cv.imshow('Blur',imgBlur)
cv.imshow('Canny',imgCanny)
cv.imshow('Dialation',imgDialation)
cv.imshow('Eroded',imgEroded)
cv.waitKey(0)