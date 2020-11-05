"""Face Detection"""


import cv2 as cv
import numpy as np
import os


file_path = os.path.dirname(__file__)

face_cascade = cv.CascadeClassifier(file_path+'/haarcascade_frontalcatface.xml')

img = cv.imread(file_path+'/face2.jpg')

imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)


faces = face_cascade.detectMultiScale(imgGray,1.1,4)


for (x, y, w, h) in faces:
    cv.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)

cv.imshow('Face',img)


cv.waitKey(0)


