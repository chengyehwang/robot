#!/usr/bin/env python3
import cv2
from tracker import *
import time

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

        # Extract Region of interest
        roi = frame.copy()

        # 1. Object Detection
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if y > 50:
                continue
            if area < 500:
                continue
            if w / h > 2:
                continue
            if h / w > 2:
                continue
            if True:
                detections.append([x, y, w, h])

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
        cv2.imshow("Mask", cv2.pyrDown(mask))
        cv2.moveWindow("Mask", int(width/2), 0)
        cv2.imshow("roi", cv2.pyrDown(roi))
        cv2.moveWindow("roi", 0, int(height/2)+20)

        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    track()

