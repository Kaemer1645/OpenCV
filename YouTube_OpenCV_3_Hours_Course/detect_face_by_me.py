"""Face Detection"""


import cv2 as cv
import os


file_path = os.path.dirname(__file__)

face_cascade = cv.CascadeClassifier(file_path+'/haarcascade_frontalcatface.xml')

webcam = cv.VideoCapture(0)

while True:

    success, img = webcam.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv.imshow('Face', img)
    if cv.waitKey(15) & 0xFF == ord('q'):
        break












