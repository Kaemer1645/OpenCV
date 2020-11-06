"""Number Plate Detection"""

import cv2 as cv
import os

file_path = os.path.dirname(__file__)
plateCascade = cv.CascadeClassifier(file_path + '/haarcascade_russian_plate_number.xml')

img = cv.imread(file_path+'/car.jpg')
imageHeight, imageWidth = img.shape[:2]

minArea = 500
color = (0,255,0)
count = 0



#img = cv.resize(img,(imageWidth,imageHeight))


while True:
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.putText(img,'NumberPlate',(x,y-5),cv.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)


            #region of number plate
            imgRoi = img[y:y+h,x:x+w]
            cv.imshow("NumberPlate",imgRoi)

    cv.imshow('Car', img)
    #cv.waitKey(0)
    if cv.waitKey(0) & 0xFF == ord('s'):
        cv.imwrite(file_path+'/ScanFolder/NoPlate_'+str(count)+'.jpg',imgRoi)
        cv.rectangle(img,(0,200),(imageWidth,imageHeight-200),(0,255,0),cv.FILLED)
        cv.putText(img,'Scan Saved',(150,265),cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),2)
        cv.imshow('Car',img)
        cv.waitKey(500)
        count += 1
    elif 0xFF == ord('q'):
        break
