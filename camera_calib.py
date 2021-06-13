#!/usr/bin/env python3
import numpy as np
import cv2 as cv
import glob

from control import *
from arm import *
import os

width = 7
height = 5

def calib_do():
    image_file = 'board_%d_%d.jpg'%(width, height)
    os.system('./gen_pattern.py -c %d -r %d -T checkerboard -o %s'%(width, height, image_file))
    adb_dut('rm /storage/emulated/0/DCIM/Screenshots/%s'%image_file)
    adb_cmd('push %s /storage/emulated/0/DCIM/Screenshots/'%image_file)
    adb_dut('am start -a android.intent.action.VIEW -d file:///storage/emulated/0/DCIM/Screenshots/%s -t image/jpeg'%image_file)
    screen('calib/1.jpg')

def calib_post():
    print('height', height, 'width', width)
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((height*width,3), np.float32)
    objp[:,:2] = np.mgrid[0:height,0:width].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('calib/*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        (thresh, gg) = cv2.threshold(gray, 127, 255, cv.THRESH_BINARY)
        cv.imshow('gray', gray)
        cv.imshow('gg', gg)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (height-1,width-1), None )
        # If found, add object points, image points (after refining them)
        if ret == True:
            print('chessboard is found')
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (height-1,width-1), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.waitKey(5000)
    cv.destroyAllWindows()


def comp():
    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite('calibresult.png', dst)


if __name__ == "__main__":
    width = 9
    height = 15
    #calib_do()
    calib_post()

