import cv2 as cv
import os
import numpy as np

webcam = cv.VideoCapture(0)

webcam.set(3,640)
webcam.set(4,480)
while True:
    success, img = webcam.read()
    imgCanny = cv.Canny(img, 100, 100)
    cv.imshow('WebCam',imgCanny)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break