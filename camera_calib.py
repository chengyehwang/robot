#!/usr/bin/env python3
import numpy as np
import cv2 as cv
import glob

from control import *
from arm import *
import os

def calib_do():
    os.system('./gen_pattern.py -c 7 -r 5 -T checkerboard -o checkerboard.jpg')
    adb_dut('rm /storage/emulated/0/Download/checkerboard.jpg')
    adb_cmd('push checkerboard.jpg /storage/emulated/0/Download/')
    adb_dut('am start -a android.intent.action.VIEW -d file:///storage/emulated/0/Download/checkerboard.jpg -t image/jpeg')
    screen('calib/1.jpg')

def calib_post():
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
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
        ret, corners = cv.findChessboardCorners(gray, (4,6), None )
        # If found, add object points, image points (after refining them)
        if ret == True:
            print('chessboard is found')
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (7,6), corners2, ret)
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
    calib_do()
    calib_post()
