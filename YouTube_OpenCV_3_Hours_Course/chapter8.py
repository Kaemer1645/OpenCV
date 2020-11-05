"""Contour - Shape Detection"""
import cv2 as cv
import numpy as np
import os

def getContours(img):

    #external - outer details in RETR EXTERNAL
    #aprox chain - give us all elemtns non compress in one detail

    contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        print(area)
        #contourldx draw all the contour
        if area >500:
            cv.drawContours(imgContour, cnt, -1, (252, 132, 3), 3)
            perimeter  = cv.arcLength(cnt,True) #true bcs its closed
            print(perimeter)

            #aprox corner points
            approx = cv.approxPolyDP(cnt, 0.02*perimeter, True)
            print(len(approx))
            objCor = len(approx)


            x, y , w, h = cv.boundingRect(approx)
            print(x,y,w,h)

            if objCor == 3: objectType = 'Triangle'
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05: objectType = 'Square' #we give 5% error for pixels
                else: objectType = 'Rectangle'
            elif objCor > 4: objectType = 'Circle'
            else: objectType = 'None'
            cv.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv.putText(imgContour, objectType,(x+(w//2)-10,y+(h//2)),
                       cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1) #-10 is reduced 10 pixels






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


file_path = os.path.dirname(__file__)

img = cv.imread(file_path+'/shapes.jpg')
imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
imgBlur = cv.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv.Canny(imgBlur,100,300)
imgContour = img.copy()

getContours(imgCanny)


blank = np.zeros_like(img)
stacked = stackImages(1,([img,imgGray,imgBlur],[imgCanny,imgContour,blank]))
cv.imshow('Stacked',stacked)

cv.waitKey(0)