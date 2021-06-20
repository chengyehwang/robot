#!/usr/bin/env python3
import numpy as np
import cv2 as cv
import glob
import simplejson as json

from control import *
from arm import *
import os

width = 9
height = 17

def calib_do():
    image_path = '/storage/emulated/0/DCIM/Camera/'
    image_file = 'board_%d_%d.jpg'%(width, height)
    os.system('./gen_pattern.py -c %d -r %d -T checkerboard -o %s'%(width, height, image_file))
    adb_dut('rm %s/board_*_*.jpg'%image_path)
    adb_cmd('push %s %s'%(image_file, image_path))
    adb_dut('am start -a android.intent.action.VIEW -d file://%s%s -t image/jpeg'%(image_path, image_file))
    time.sleep(1)
    adb_dut('input tap 500 500')
    time.sleep(1)
    screen('calib.jpg')

def calib_post():
    print('height', height, 'width', width)
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros(((height-1)*(width-1),3), np.float32)
    objp[:,:2] = np.mgrid[0:height-1,0:width-1].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    if True:
        fname = 'calib.jpg'
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imshow('gray', gray)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (height-1,width-1), None )
        # If found, add object points, image points (after refining them)
        if ret == True:
            print('chessboard is found')
            objpoints.append(objp)
            cross = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (height-1,width-1), cross, ret)
            cv.imshow('img', img)
            
    cv.waitKey()
    cv.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    print(mtx,dist)

    pos0 = cross[0][0]
    pos1 = cross[height-1-1][0]
    pos2 = cross[(height-1)*(width-1)-1][0]
    src_rot = np.matrix([pos0, pos1, pos2]).astype(np.float32)
    dst_rot = np.matrix([[pos0[0],pos1[1]], pos1, [pos1[0], pos2[1]]]).astype(np.float32)
    matrix_rot = cv.getAffineTransform(src_rot, dst_rot)
    print(src_rot, dst_rot, matrix_rot)

    with open('calib.json', 'w') as fp:
        fp.write(json.dumps({'mtx':mtx.tolist(),'dist':dist.tolist(),'rot': matrix_rot.tolist()},indent=4))

def comp(img=[]):
    with open('calib.json') as fp:
        calib = json.load(fp)
    mtx = np.matrix(calib['mtx'])
    dist = np.matrix(calib['dist'])
    rot = np.matrix(calib['rot'])
    #print('mtx', mtx, 'dist', dist, 'rot', rot)
    # undistort
    dst = cv.undistort(img, mtx, dist, None, None)
    # rotate

    dst_wrap = cv.warpAffine(dst, rot, (dst.shape[1], dst.shape[0]))
    # crop the image
    return dst_wrap


if __name__ == "__main__":
    if True:
        #calib_do()
        #calib_post()
        data = screen('')
        print(data)
        data_new = comp(data)
        cv.imshow('orig', data)
        cv.imshow('new', data_new)
        cv.waitKey()
        cv.destroyAllWindows()
