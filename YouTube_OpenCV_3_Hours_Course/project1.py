"""project 1 Virtual Painting"""

import cv2 as cv
import numpy as np


cap = cv.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
#red,orange, green
myColors = [[108, 119, 0, 179, 189, 255],
            [0,105,35,7,166,255],
            [46, 80, 0, 96, 176, 255]]
            #yellow [23,31,0,57,102,255]

myColorValues = [[0,17,255],[0,128,255],[26,255,0]]


myPoints = [] #[x, y, colorID]

def drawer(myPoints, myColorValues):
    for point in myPoints:
        cv.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv.FILLED)




def findColor(img, myColors, myColorValues):
    imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHSV,lower,upper)
        x, y = getContours(mask)
        cv.circle(imgResult,(x,y),10,myColorValues[count],cv.FILLED)
        if x!= 0 and y!=0:
            newPoints.append([x,y,count])

        count += 1
    return newPoints
        #cv.imshow(str(color[0]),mask)
def getContours(img):

    #external - outer details in RETR EXTERNAL
    #aprox chain - give us all elemtns non compress in one detail

    contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        #contourldx draw all the contour
        if area >500:
            cv.drawContours(imgResult, cnt, -1, (252, 132, 3), 3)
            perimeter  = cv.arcLength(cnt,True) #true bcs its closed

            #aprox corner points
            approx = cv.approxPolyDP(cnt, 0.02*perimeter, True)
            x, y , w, h = cv.boundingRect(approx)
    return x+w//2, y

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawer(myPoints,myColorValues)

    cv.imshow('WebCam',imgResult)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break



#Zaczac od 2:10 w filmie