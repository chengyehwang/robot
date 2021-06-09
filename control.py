#!/usr/bin/env python
import os
import re
from subprocess import PIPE, Popen

device_dut = None
device_mon = None

def adb_cmd(cmd, **kwargs):
    dut = kwargs.get('dut',False)
    mon = kwargs.get('mon',False)
    global device_dut
    global device_mon
    if dut:
        cmd = 'adb -s ' + device_dut + ' ' + cmd
    elif mon:
        cmd = 'adb -s ' + device_mon + ' ' + cmd
    else:
        cmd = 'adb ' + cmd
    print(cmd)
    process = Popen(
        args=cmd,
        stdout=PIPE,
        shell=True
    ).stdout
    return process.read().decode().split('\r\n')
def adb_shell (cmd, **kwargs):
    dut = kwargs.get('dut',False)
    mon = kwargs.get('mon',False)
    global device_dut
    global device_mon
    if dut and not device_dut or mon and not device_mon:
        outs = adb_cmd('devices')
        for line in outs:
            m = re.search('(\S+)\s+device', line)
            if m:
                device = m.group(1)
                if len(device) > 10:
                    device_dut = device
                else:
                    device_mon = device
        print(device_dut, device_mon)
    
    if dut:
        return adb_cmd('-s ' + device_dut + ' shell "' + cmd + '"')
    if mon:
        return adb_cmd('-s ' + device_mon + ' shell "' + cmd + '"')

def adb_dut(cmd):
    return adb_shell(cmd, dut = True)
def adb_mon(cmd):
    return adb_shell(cmd, mon = True)

#adb_mon('input keyevent POWER')
adb_mon('input keyevent WAKEUP')
adb_mon('input keyevent FOCUS')
adb_mon('input keyevent KEYCODE_CAMERA')
adb_mon('input swipe 300 1000 300 100')
print(adb_mon('am start -a android.media.action.IMAGE_CAPTURE --ei android.intent.extras.CAMERA_FACING 0'))
adb_cmd('push scroll.sh /data/local/tmp', dut=True)
adb_dut('chmod 755 /data/local/tmp/scroll.sh')
adb_dut('dos2unix /data/local/tmp/scroll.sh')
adb_dut('nohup /data/local/tmp/scroll.sh >/dev/null 2>/dev/null &')
