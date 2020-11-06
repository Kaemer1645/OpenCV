"""Document Scanner"""
import cv2 as cv
import numpy as np
import os

#cap = cv.VideoCapture(0) #0 is id of camera in your laptop
# the id's of height, width, brightness is here https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
#imageWidth = 480
#imageHeight = 640

# cap.set(3,imageWidth)
# cap.set(4,imageWidth)
# cap.set(10,150)
file_path = os.path.dirname(__file__)
img = cv.imread(file_path + '/document.jpg')
imageHeight, imageWidth = img.shape[:2]


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver






def getContours(img):
    biggest = np.array([])
    maxArea = 0
    #external - outer details in RETR EXTERNAL
    #aprox chain - give us all elemtns non compress in one detail

    contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        #cv.drawContours(imgContour, cnt, -1, (252, 132, 3), 3)
        area = cv.contourArea(cnt)
        #contourldx draw all the contour
        if area >5000:
            perimeter  = cv.arcLength(cnt,True) #true bcs its closed

            #aprox corner points
            approx = cv.approxPolyDP(cnt, 0.02*perimeter, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv.drawContours(imgContour, biggest, -1, (252, 132, 3), 3)

    return biggest


def sorter(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    #print('add',add)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    #print("New points",myPointsNew)
    return myPointsNew



def getWarp(img, biggest):
    biggest = sorter(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [imageWidth, 0], [0, imageHeight], [imageWidth, imageHeight]])

    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img, matrix, (imageWidth, imageHeight))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv.resize(imgCropped,(imageWidth,imageHeight))

    return imgCropped

def preProcessing(img):
    imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv.Canny(imgBlur,150,150)
    kernel = np.ones((3,3))
    imgDial = cv.dilate(imgCanny,kernel,iterations=2)
    imgErode = cv.erode(imgDial,kernel,iterations =1)

    return imgErode


while True:
    #success, img = cap.read()

    img = cv.resize(img,(imageWidth,imageHeight))
    imgContour = img.copy()
    imgThreshold = preProcessing(img)
    #cv.imshow('img',imgThreshold)
    biggest = getContours(imgThreshold)
    if biggest.size != 0:
        imgWarped = getWarp(img,biggest)
        cv.imshow('Stacked',stackImages(0.6,[img,imgThreshold,imgWarped]))
    else:
        cv.imshow('Stacked', stackImages(0.6, [img, img, img]))
    #cv.imshow('WebCam',imgWarped)
    #cv.imshow('WebCam',img)
    if cv.waitKey(0) & 0xFF == ord('q'):
        break




