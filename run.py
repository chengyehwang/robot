#!/usr/bin/env python3
from camera_calib import *
from control import *
from gcode import *
from arm import *
from multiprocessing import Process
from motion import *
import os
if False:
    gcode_begin()
    gcode_kernel("$x\n$h\nG92 X0Y0Z0\nG90\n".split('\n'))
    gcode_end()
    calib_do()
    calib_post()
if False:
    gcode_begin()
    gcode_kernel("$x\n$h\nG92 X0Y0Z0\nG90\n".split('\n'))
    fps_begin()
    launch_package()
    p = Process(target = video, args = ('test.avi',))
    p.start()
    for i in range(20):
        pass
        gcode_kernel("G01 X230Y-120F10000\nG01 Z-20F1000\nG01 X230Y-30F5000\nG01 Z0F4000\n".split('\n'))

    p.join()
    fps_end()
    fps_plot()

if True:
    track()

