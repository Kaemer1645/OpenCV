import cv2 as cv
import subprocess
import time
#id of camera witch you use
cap = cv.VideoCapture(0)

face_cascade=cv.CascadeClassifier(r'D:\STUDIA\Programowanie\Skrypt_wykrycie_twarzy\haarcascade_frontalface_default.xml')
eye_cascade=cv.CascadeClassifier(r'D:\STUDIA\Programowanie\Skrypt_wykrycie_twarzy\haarcascade_eye.xml')

iterator = 0
while True:
    ret, frame = cap.read()
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    print(str(len(faces)))


    for (x,y,w,h) in faces:
        cv.rectangle(frame,(x,y),(x+w, y+h),(255,0,0),2)
        eye_gray=gray[y:y+h,x:x+w]
        eye_color=frame[y:y+h,x:x+w]
        eyes=eye_cascade.detectMultiScale(eye_gray)
        for (ex,ey,ew,eh) in eyes:
            cv.rectangle(eye_color, (ex,ey),(ex+ew,ey+eh),(0,255,0),2)




    cv.imshow('frame',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    if len(faces) == 1:
        iterator += 1
        if iterator == 30:
            subprocess.Popen(['start', r'C:\Windows\Media\Alarm01.wav'], shell=True)
            iterator=-80
            print('Alarm --- Zlodziej!!!')
            continue

cv.destroyAllWindows()



