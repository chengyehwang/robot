#!/usr/bin/env python3
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
    return process.read().decode().split(os.linesep)
def adb_shell (cmd, **kwargs):
    dut = kwargs.get('dut',False)
    mon = kwargs.get('mon',False)
    global device_dut
    global device_mon
    if dut and not device_dut or mon and not device_mon:
        outs = adb_cmd('devices')
        for line in outs:
            print('line', line)
            m = re.search('(\S+)\s+device$', line)
            if m:
                device = m.group(1)
                if len(device) > 10:
                    device_dut = device
                else:
                    device_mon = device
        print('dut', device_dut, 'mon', device_mon)
    
    if dut:
        return adb_cmd('-s ' + device_dut + ' shell "' + cmd + '"')
    if mon:
        return adb_cmd('-s ' + device_mon + ' shell "' + cmd + '"')

def camera_file(cmd):
    dir = '/sdcard/DCIM/Camera'
    out = adb_mon('ls -t %s'%dir)
    file = out[0]
    adb_cmd('pull %s/%s'%(dir,file),mon=True)

def adb_dut(cmd):
    return adb_shell(cmd, dut = True)
def adb_mon(cmd):
    return adb_shell(cmd, mon = True)

#camera_file('')

def list_package(name):
    packages = adb_dut('pm list packages -f')
    for p in packages:
        m = re.search('.*=(.*)',p)
        if m:
            package = m.group(1)
            if name in package:
                return (package)

def fps_begin():
    package = list_package('baidu')
    adb_dut('dumpsys gfxinfo %s reset'%package)
def fps_end():
    package = list_package('baidu')
    out = adb_dut('dumpsys gfxinfo %s'%package)
    with open('gfxinfo','w') as fp:
        fp.write('\n'.join(out))

if __name__ == '__main__':

    #adb_mon('input keyevent POWER')
    #adb_mon('input keyevent WAKEUP')
    #adb_mon('input keyevent FOCUS')
    #adb_mon('input keyevent KEYCODE_CAMERA')
    #adb_mon('input swipe 300 1000 300 100')
    #print(adb_mon('am start -a android.media.action.IMAGE_CAPTURE --ei android.intent.extras.CAMERA_FACING 0'))
    if False:
        adb_cmd('push scroll.sh /data/local/tmp', dut=True)
        adb_dut('chmod 755 /data/local/tmp/scroll.sh')
        adb_dut('dos2unix /data/local/tmp/scroll.sh')
        adb_dut('nohup /data/local/tmp/scroll.sh >/dev/null 2>/dev/null &')
    fps_begin()
    if True:
        with open("scroll_test.gcode", "w") as fp:
            fp.write("$x\n$h\nG92 X0Y0Z0\nG90\n")
            for i in range(20):
                fp.write("G01 X50Y-120F10000\nG01 Z-20F1000\nG01 X50Y-30F12000\nG01 Z0F4000\n")

        os.system('python3 gcode.py --gcode_file scroll_test.gcode')
    fps_end()

