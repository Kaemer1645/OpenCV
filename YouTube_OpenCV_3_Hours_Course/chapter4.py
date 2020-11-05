"""Work with shapes and texts"""

import cv2 as cv
import os
import numpy as np

#below 3 means 3 channels
img = np.zeros((512,512,3),np.uint8)

#[:] is entire image

#img[:]= 255,0,0

#slice of image - and coloring
#img[200:300,400:512] = 89,100,89

#create lines
cv.line(img,(0,0),(100,300),color=(0,0,255),thickness=1,lineType=cv.LINE_AA)
cv.rectangle(img,(0,0),(100,300),color=(0,0,255),thickness=3)
cv.circle(img,(int(img.shape[1]/2),int(img.shape[0]/2)),40,(0,255,20),thickness=cv.FILLED)
cv.putText(img," OPEN CV ",(300,200),cv.FONT_HERSHEY_COMPLEX,1,(160,33,220))


cv.imshow('Image',img)

cv.waitKey(0)


