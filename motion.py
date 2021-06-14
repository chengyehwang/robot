#!/usr/bin/env python3
import cv2
from tracker import *
import time
from camera_calib import *
def track():
    # Create tracker object
    tracker = EuclideanDistTracker()

    cap = cv2.VideoCapture("test.avi")

    # Object detection from Stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    now_prev = time.time()
    while True:
        ret, frame = cap.read()
        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

        print(width, height)

        if not ret:
            break

        # calib comp
        roi = comp(frame)

        # 1. Object Detection
        #mask = object_detector.apply(roi)
        #_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if area < 500:
                continue
            if True:
                detections.append([x, y, w, h])

        can = cv.Canny(gray, 50, 200, None, 3)
        lines = cv.HoughLines(can, 1, np.pi / 180, 150, None, 0, 0)
        for line in lines:
            rho = line[0][0]
            theta = line[0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            if abs(b) > 0.1:
                continue
            cv.line(roi, pt1, pt2, (0,0,255), 3)

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        now = time.time()
        delta = now - now_prev
        now_prev = now
        if delta < 0.5:
            time.sleep(0.5 - delta)

        cv2.imshow("Frame", cv2.pyrDown(frame))
        cv2.moveWindow("Frame", 0, 0)
        cv2.imshow("gray", cv2.pyrDown(gray))
        cv2.moveWindow("gray", int(width/2), 0)
        cv2.imshow("roi", cv2.pyrDown(roi))
        cv2.moveWindow("roi", 0, int(height/2)+20)
        cv2.imshow("can", cv2.pyrDown(can))
        cv2.moveWindow("can", int(width/2), int(height/2)+20)

        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    track()

