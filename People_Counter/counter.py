"""Face Detection"""


import cv2 as cv
import os


file_path = os.path.dirname(__file__)

face_cascade = cv.CascadeClassifier(file_path+'/haarcascade_fullbody.xml')

#webcam = cv.VideoCapture(0)
src = cv.imread(file_path+'/kobieta_sylwetka.jpg')

'''scale_percent = 30

#calculate the 50 percent of original dimensions
width = int(src.shape[1] * scale_percent / 100)
height = int(src.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)

# resize image
img_silu = cv.resize(src, dsize)'''

while True:

    img = src
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    body = face_cascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in body:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv.imshow('Body', img)
    if cv.waitKey(15) & 0xFF == ord('q'):
        break












