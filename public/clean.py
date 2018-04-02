# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
import lib.Utils as U
import lib.Logging as L
import os
import public.adb
def clean_device_yaml():
    ini = U.ConfigIni()
    device_yaml = ini.get_ini('test_device','device')
    if os.path.getsize(device_yaml):
        with open(device_yaml,'w') as f:
            f.truncate()
            f.close()
        return
    return
def clean_logcat(device):
    pid = U.cmd('netstat -aon | findstr %s' % device).stdout.readline().strip().split(' ')[-1]
    U.cmd('taskkill /f /pid %s' % pid)
    U.sleep(2)
    L.Logging.success('stop logcat %s' % device)
def clean_appium(port,device):
    #for line in U.cmd('netstat -aon | findstr %d' % port).stdout.readlines():
    line = U.cmd('netstat -aon | findstr %d' % port).stdout.readline()
    pid = line.strip().split(' ')[-1]
    U.cmd('taskkill /f /pid {}'.format(pid))
    L.Logging.success("killed appium %s" % port)
    clean_logcat(device)
    reconnect_device(device)
def reconnect_device(device):
    adb = public.adb.adb()
    adb.connect(device)
    U.sleep(3)
    L.Logging.success('reconnect device %s' % device)

if __name__ == '__main__':
    #print 'rrrd'
   # clean_device_yaml()
   #clean_appium(4723)
   reconnect_device('192.168.1.109:5555')
