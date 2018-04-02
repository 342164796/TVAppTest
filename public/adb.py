# -*- coding:utf-8 -*-
import subprocess
import sys
sys.path.append('..')
import lib.Utils as U
import os
import re
class adb():
    def __init__(self,device=''):
        if device =='':
            self.device = ''
        else:
            self.device = "-s %s" % device
    def adb(self,args):
        return U.cmd('adb %s %s' % (self.device,str(args)))
    def logcat(self,log_path):
        return self.adb('logcat -v time > %s&' % log_path)
    def logcat_c(self):
        return self.adb('logcat -c')
    def shell(self,args):
        cmd = 'adb %s shell %s' %(self.device,str(args))
        return U.cmd(cmd)
    def connect(self,device):
        device = device.split(':')[0]
        return U.cmd('adb connect %s' % device)
    def get_cpu(self,package_name):
        p = self.shell('top -n 1 -d 0.5 | findstr %s' % package_name)
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r.endswith(package_name):
                lst = []
                for i in r.split(' '):
                    if i:
                        lst.append(i)
                return int(lst[2].split('%',1)[0])
    def get_current_app_mem(self,package_name):
        p = self.shell('top -n 1 -d 0.5 | findstr %s' % package_name)
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r.endswith(package_name):
                lst = []
                for i in r.split(' '):
                    if i:
                        lst.append(i)
                return int(lst[6].split('K')[0])
    def get_total_mem(self):
        p = self.shell('cat proc/meminfo')
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r and 'MemTotal' in r:
                lst = []
                for i in r.split(' '):
                    if i:
                        lst.append(i)
                return int(lst[1])
    def get_mem(self,package_name):
        try:
            return int(self.get_current_app_mem(package_name) / float(self.get_total_mem())*100)
        except:
            return None
    def get_sceenshot(self,screen_file):
        os.system('adb %s shell screencap -p /data/local/tmp/screencap.png' % self.device)
        os.system('adb %s pull /data/local/tmp/screencap.png %s' %(self.device,screen_file))
        return screen_file
    def get_app_version(self,packageName):
        for line in self.shell('dumpsys package %s' % packageName).stdout.readlines():
            if 'versionName' in line:
                return line.split('=',2)[1].strip()
    def get_device_name(self):
        t = self.shell('getprop ro.product.model').stdout.readlines()
        return ''.join(t).strip()
    def get_disk(self):
        for s in self.shell('df').stdout.readlines():
            if '/data' in s:
                lst=[]
                for i in s.split(' '):
                    if i:
                        lst.append(i)
                return 'Used:%s, Free:%s' % (lst[2],lst[3])
    def get_wifi_name(self):
        for line in self.shell('dumpsys wifi').stdout.readlines():
            if line.startswith('mWifiInfo'):
                wifi_name = re.findall(r'SSID:([^"]+), BSSID',line)
                if not wifi_name:
                    return None
                else:
                    return wifi_name[0].strip()
    def get_android_version(self):
        return self.shell('getprop ro.build.version.release').stdout.read().strip()
    def get_screen_resolution(self):
        pattern = re.compile(r"\d+")
        out = self.shell("dumpsys display | findstr PhysicalDisplayInfo" ).stdout.read()
        display = pattern.findall(out)
        if display:
            return int(display[0]),int(display[1])
        else:
            return 1920,1080
if __name__ == '__main__':
    s = adb('192.168.1.100:5555')
    print s.get_screen_resolution()
