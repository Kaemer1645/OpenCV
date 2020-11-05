"""Resize and Cropping"""
import cv2 as cv
import os
import numpy as np

file_path = os.path.dirname(__file__)

img = cv.imread(file_path+'/landscape.jpg')
#height, width, chanels
print(img.shape)

#resize
#in cv we have width, height
imgResize = cv.resize(img,(300,600))

#crop - here height comes first
imgCropped = img[0:200,400:700]

#display
cv.imshow('snake',img)
cv.imshow('Resized',imgResize)
cv.imshow('Cropped',imgCropped)

cv.waitKey(0)