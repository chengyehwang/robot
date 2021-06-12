#!/usr/bin/env python3

from gcode import *

def init():
    gcode_begin()
    lines = ['$x','$h','G92 X0Y0Z0','G90']
    gcode_kernel(lines)

def scroll(x,y):

    lines = ['G01 X50Y-120F10000',
            'G01 Z-20F1000',
            'G01 X50Y-30F8000',
            'G01 Z0F4000']
    gcode_kernel(lines)

def click(x,y):

    x = 50 + x
    y = -20 - y
    lines = ['G01 X%dY%dF10000'%(x,y),
            'G01 Z-20F4000',
            'G01 Z0F4000']
    gcode_kernel(lines)

def end():    
    gcode_end()

init()
for y in range(0, 100, 5):
    for x in range(0, 50, 5):
        click(x,y)
end()

