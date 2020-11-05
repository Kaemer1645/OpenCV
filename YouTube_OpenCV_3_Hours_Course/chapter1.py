"""Work with images, webcam and videos"""
import cv2 as cv
import os

file_path = os.path.dirname(__file__)



''' # images
img = cv.imread(file_path+'/snake.jpg')
cv.imshow('snake',img)
cv.waitKey(0) #0  is infinite loop, other values are in miliseconds 1000 is 1 sec'''


'''#videos

cap = cv.VideoCapture(file_path+'/test.mp4')

while True:
    success, img = cap.read()
    cv.imshow('Video',img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break'''



#WebCam

cap = cv.VideoCapture(0) #0 is id of camera in your laptop
# the id's of height, width, brightness is here https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)

while True:
    success, img = cap.read()
    cv.imshow('WebCam',img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break