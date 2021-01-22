import cv2
import requests
import numpy as np


def ip_webcam():
    URL = "http://192.168.0.108:8080/shot.jpg"
    while True:
        img_request = requests.get(URL)
        img_arr = np.array(bytearray(img_request.content), dtype=np.uint8)
        #img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        cv2.imshow('IPWebcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

