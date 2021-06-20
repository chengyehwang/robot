#!/usr/bin/env python3
import math
import time
import cv2
import os
from Arm_Lib import Arm_Device
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

def screen(file_name):
    print('screen dump to %s'%file_name)
    image = cv2.VideoCapture(0)
    ret, frame = image.read()
    if file_name == '':
        return frame
    value = bgr8_to_jpeg(frame)
    with open(file_name, 'wb') as fp:
        fp.write(value)
    image.release()

def video(file_name):
    os.system('v4l2-ctl --set-parm=60 --set-fmt-video=width=640,height=480,pixelformat=MJPG --stream-mmap --stream-count=240 --stream-to=test.raw')
    fps = 90
    cap = cv2.VideoCapture('test.raw')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #fps = cap.get(cv2.CAP_PROP_FPS)
    print('fps',fps,'width',width,'height',height)
    out = cv2.VideoWriter(file_name, fourcc, fps, (int(width), int(height)))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret ==True:
            out.write(frame)
        else:
            break
    cap.release()
    out.release()

def video_mirror():
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('img', frame)
        result = cv2.waitKey(100)
        if result > 0:
            break
    cap.release()

def video_cv(file_name):
    cap = cv2.VideoCapture(0+cv2.CAP_V4L2)
    fps = 60
    result = cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    result = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    result = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    result = cap.set(cv2.CAP_PROP_FPS, fps)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('fps:',fps,'width',width,'height', height)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(file_name, fourcc, fps, (int(width), int(height)))
    start = time.time()
    frame_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_count += 1
        now = time.time()
        if ret ==True:
            pass
            #out.write(frame)
        else:
            break
        if ( now - start ) > 20.0:
            print('20s %d frame'%frame_count)
            break
    cap.release()
    out.release()

Arm = Arm_Device()
def hold():
    global Arm
    time.sleep(.1)
    Arm.Arm_serial_servo_write(1, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(2, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(3, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(4, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(5, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(6, 90, 500)
    time.sleep(0.5)

def stop():
    global Arm
    Arm.Arm_serial_servo_write(1, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(2, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(3, 0, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(4, 0, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(5, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(6, 90, 500)
    time.sleep(0.5)

def mon():
    Arm.Arm_serial_servo_write(1, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(2, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(3, 0, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(4, 0, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(5, 90, 500)
    time.sleep(0.5)
    Arm.Arm_serial_servo_write(6, 180, 500)
    time.sleep(0.5)

if __name__ == '__main__':
    if False:
        hold()
        time.sleep(1)
        mon()
    if False:
        mon()
    if False:
        video('test.avi')
    if True:
        video_mirror()
