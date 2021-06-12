#!/usr/bin/env python3

from gcode import *
from control import *

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

def get_input():
    x = 0
    y = 0
    lines = adb_dut('timeout 2 getevent')
    print('\n'.join(lines))
    for line in lines:
        if '0035' in line:
            e = line.split(" ")
            x = e[3]
            x = int(x, 16)
        if '0036' in line:
            e = line.split(" ")
            y = e[3]
            y = int(y, 16)

    return (x,y)

init()
data = {}
for y in range(0, 100, 20):
    for x in range(0, 50, 10):
        click(x+3,y+3)
        click(x,y)
        pos = get_input()
        print(pos)
        data[(x,y)] = pos

print(data)
end()

