"""Warp perspective"""
import cv2 as cv
import numpy as np
import os

file_path = os.path.dirname(__file__)


img = cv.imread(file_path+'/cards.jpg')

width, height = 250,350

#width, height
pts1 = np.float32([[225,91],[430,133],[161,385],[371,426]])
pts2 = np.float32([[0,0],[width, 0],[0,height],[width,height]])

matrix = cv.getPerspectiveTransform(pts1,pts2)
imgOutput = cv.warpPerspective(img,matrix,(width,height))

cv.imshow('cards',img)
cv.imshow('Transformed',imgOutput)

cv.waitKey(0)