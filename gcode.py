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
ENABLE_STATUS_REPORTS = False
REPORT_INTERVAL = 1.0 # seconds

is_run = True # Controls query timer

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
verbose = True
if args.quiet : verbose = False

# Wake up grbl
print ("Initializing Grbl...")
s.write(bytes("\r\n\r\n",'ascii'))

# Wait for grbl to initialize and flush startup text in serial input
time.sleep(2)
s.flushInput()
l_count = 0
if True:
    # Send g-code program via a more agressive streaming protocol that forces characters into
    # Grbl's serial read buffer to ensure Grbl has immediate access to the next g-code command
    # rather than wait for the call-response serial protocol to finish. This is done by careful
    # counting of the number of characters sent by the streamer to Grbl and tracking Grbl's 
    # responses, such that we never overflow Grbl's serial read buffer. 
    g_count = 0
    c_line = []
    for line in f:
        l_count += 1 # Iterate line counter
        l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
        # l_block = line.strip()
        c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
        grbl_out = '' 
        while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
            out_temp = str(s.readline().strip()) # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                print ("    MSG: \""+out_temp+"\"") # Debug response
            else :
                if out_temp.find('error') >= 0 : error_count += 1
                g_count += 1 # Iterate g-code counter
                if verbose: print ("  REC<"+str(g_count)+": \""+out_temp+"\"")
                del c_line[0] # Delete the block character count corresponding to the last 'ok'
        s.write(bytes(l_block + '\n','ascii')) # Send g-code block to grbl
        if verbose: print ("SND>"+str(l_count)+": \"" + l_block + "\"")
    # Wait until all responses have been received.
    while l_count > g_count :
        out_temp = str(s.readline().strip()) # Wait for grbl response
        if out_temp.find('ascii') < 0 and out_temp.find('error') < 0 :
            print ("    MSG: \""+out_temp+"\"") # Debug response
        else :
            if out_temp.find('error') >= 0 : error_count += 1
            g_count += 1 # Iterate g-code counter
            del c_line[0] # Delete the block character count corresponding to the last 'ok'
            if verbose: print ("  REC<"+str(g_count)+": \""+out_temp + "\"")

# Wait for user input after streaming is completed
print ("\nG-code streaming finished!")
end_time = time.time();
is_run = False;
print (" Time elapsed: ",end_time-start_time,"\n")
if check_mode :
    if error_count > 0 :
        print ("CHECK FAILED:",error_count,"errors found! See output for details.\n")
    else :
        print ("CHECK PASSED: No errors found in g-code program.\n")
else :
   print ("WARNING: Wait until Grbl completes buffered g-code blocks before exiting.")
   raw_input("  Press <Enter> to exit and disable Grbl.") 

# Close file and serial port
f.close()
s.close()
