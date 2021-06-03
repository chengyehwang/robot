#!/usr/bin/env python

import serial
import re
import time
import sys
import argparse
import threading

DEVICE_FILE = 'COM5'
RX_BUFFER_SIZE = 128
BAUD_RATE = 115200


# Define command line argument interface
parser = argparse.ArgumentParser(description='python library')
parser.add_argument('gcode_file', type=argparse.FileType('r'),
        help='g-code filename to be streamed')
parser.add_argument('-q','--quiet',action='store_true', default=False, 
        help='suppress output text')
args = parser.parse_args()

# Initialize
s = serial.Serial(DEVICE_FILE, BAUD_RATE)
f = args.gcode_file

# Wake up grbl
print ("Initializing Grbl...")
s.write(bytes("\r\n\r\n",'ascii'))

# Wait for grbl to initialize and flush startup text in serial input
time.sleep(2)
s.flushInput()
end_time = time.time();
c_count = 0
error_count = 0
if True:
    g_count = 0
    c_line = []
    for line in f:
        c_count += 1 # Iterate line counter
        l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
        # l_block = line.strip()
        c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
        grbl_out = '' 
        while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
            out_temp = s.readline().strip().decode('ascii') # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                print ("    MSG: \""+out_temp+"\"") # Debug response
            else :
                if out_temp.find('error') >= 0 :
                    error_count += 1
                g_count += 1 # Iterate g-code counter
                print ("  REC<"+str(g_count)+": \""+out_temp+"\"")
                del c_line[0] # Delete the block character count corresponding to the last 'ok'
        s.write(bytes(l_block + '\n','ascii')) # Send g-code block to grbl
        print ("SND>"+str(c_count)+": \"" + l_block + "\"")
    # Wait until all responses have been received.
    while c_count > g_count :
        out_temp = s.readline().strip().decode('ascii') # Wait for grbl response
        if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
            print ("    MSG: \""+out_temp+"\"") # Debug response
        else :
            if out_temp.find('error') >= 0 :
                error_count += 1
            g_count += 1 # Iterate g-code counter
            del c_line[0] # Delete the block character count corresponding to the last 'ok'
            print ("  REC<"+str(g_count)+": \""+out_temp + "\"")

# Wait for user input after streaming is completed
print ("\nG-code streaming finished!")
end_time = time.time();
print (" Time elapsed: ",end_time-start_time,"\n")

# Close file and serial port
f.close()
s.close()
