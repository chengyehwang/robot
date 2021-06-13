#!/usr/bin/env python3
import math
import time
import cv2
from Arm_Lib import Arm_Device
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

def screen(file_name):
    image = cv2.VideoCapture(0)
    ret, frame = image.read()
    value = bgr8_to_jpeg(frame)
    with open(file_name, 'wb') as fp:
        fp.write(value)

def video(file_name):
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('fps:',fps)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(file_name, fourcc, fps, (640, 480))
    start = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        now = time.time()
        if ret ==True:
            out.write(frame)
        else:
            break
        if ( now - start ) > 10.0:
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
    if True:
        mon()
    if False:
        video('test.avi')
