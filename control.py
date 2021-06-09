#!/usr/bin/env python
import os
import re
from subprocess import PIPE, Popen

def adb_cmd(cmd):
    cmd = 'adb ' + cmd
    print(cmd)
    process = Popen(
        args=cmd,
        stdout=PIPE,
        shell=True
    ).stdout
    return process.read().decode().split('\r\n')

device_dut = None
device_mon = None

def adb_shell (cmd, **kwargs):
    dut = kwargs.get('dut',False)
    mon = kwargs.get('mon',False)
    global device_dut
    global device_mon
    if not device_dut or not device_mon:
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
        return adb_cmd('-s ' + device_dut + ' shell ' + cmd )
    if mon:
        return adb_cmd('-s ' + device_mon + ' shell ' + cmd )

out = adb_shell('ls',dut=True)
print('\n'.join(out))
out = adb_shell('ls',mon=True)
print('\n'.join(out))

