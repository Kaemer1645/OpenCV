#https://www.pyimagesearch.com/wp-content/uploads/2014/11/opencv_crash_course_camshift.pdf

import numpy as np
import cv2 as cv
import argparse
from ip_webcam import ip_webcam

frame = None
roiPts = []
inputMode = False

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode
    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == cv.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        cv.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv.imshow("frame", frame)

def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
    help = "path to the (optional) video file")
    args = vars(ap.parse_args())
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode
    # if the video path was not supplied, grab the reference to the
    # camera
    if not args.get("video", False):
        #camera = cv.VideoCapture(0)
        camera = cv.VideoCapture('http://192.168.0.108:8080/video')
    # otherwise, load the video
    else:
        camera = cv.VideoCapture(args["video"])
    # setup the mouse callback
    cv.namedWindow("frame")
    cv.setMouseCallback("frame", selectROI)
    # initialize the termination criteria for cam shift, indicating
    # a maximum of ten iterations or movement by a least one pixel
    # along with the bounding box of the ROI
    termination = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
    roiBox = None

    # keep looping over the frames
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        # check to see if we have reached the end of the
        # video
        if not grabbed:
            break
        # if the see if the ROI has been computed
        if roiBox is not None:
        # convert the current frame to the HSV color space
        # and perform mean shift
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            backProj = cv.calcBackProject([hsv], [0], roiHist, [0, 180], 1)
            cv.imshow('backProj', backProj)

        # apply cam shift to the back projection, convert the
        # points to a bounding box, and then draw them
            (r, roiBox) = cv.CamShift(backProj, roiBox, termination)
            pts = np.int0(cv.boxPoints(r))
            cv.polylines(frame, [pts], True, (0, 255, 0), 2)


        # show the frame and record if the user presses a key
        cv.imshow("frame", frame)
        key = cv.waitKey(1) & 0xFF
        
        # handle if the 'i' key is pressed, then go into ROI
        # selection mode
        if key == ord("i") and len(roiPts) < 4:
            # indicate that we are in input mode and clone the
            # frame
            inputMode = True
            orig = frame.copy()
        
            # keep looping until 4 reference ROI points have
            # been selected; press any key to exit ROI selction
            # mode once 4 points have been selected
            while len(roiPts) < 4:
                cv.imshow("frame", frame)
                cv.waitKey(0)
        
            # determine the top-left and bottom-right points
            roiPts = np.array(roiPts)
            s = roiPts.sum(axis=1)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]
        
            # grab the ROI for the bounding box and convert it
            # to the HSV color space
            roi = orig[tl[1]:br[1], tl[0]:br[0]]
            roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
            cv.imshow('roi_hsv',roi)
            # roi = cv.cvtColor(roi, cv.COLOR_BGR2LAB)
        
            # compute a HSV histogram for the ROI and store the
            # bounding box
            roiHist = cv.calcHist([roi], [0], None, [16], [0, 180])
            roiHist = cv.normalize(roiHist, roiHist, 0, 255, cv.NORM_MINMAX)
            roiBox = (tl[0], tl[1], br[0], br[1])

        # if the 'q' key is pressed, stop the loop
        elif key == ord("q"):
            break


    # cleanup the camera and close any open windows
    camera.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()