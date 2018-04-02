# -*- coding utf-8 -*-
import sys
sys.path.append('..')
import random
import lib.Utils as U
import lib.Logging as L
import platform
class startAppium(object):
    def __init__(self,device):
        self.device=device
    def __start_appium(self,aport,bpport):
        if platform.system() == 'Windows':
            import subprocess
            subprocess.Popen("appium -p %s -bp %s -U %s" %
                             (aport,bpport,self.device),shell=True)
        else:
            appium = U.cmd('appium -p %s -bp %s -U %s' %
                            (aport,bpport,self.device))
            while True:
                appium_line = appium.stdout.readline().strip()
                L.Logging.debug(appium_line)
                if 'listener started' in appium_line:
                    break

    def start_appium(self):
        aport = random.randint(4700, 4900)
        bpport = random.randint(4700, 4900)
        self.__start_appium(aport,bpport)
        count = 20
        for i in range(count):
            appium = U.cmd('netstat -aon | findstr %d' % aport).stdout.readline()
            if appium:
                L.Logging.debug(
                    'start appium :p %s bp %s device: %s' %
                    (aport, bpport, self.device))
                return aport
            else:
                L.Logging.info('waiting start appium 3 seconds')
                U.sleep(3)
    def main(self):
        return self.start_appium()
if __name__=='__main__':
    s=startAppium('192.168.1.107:5555')
    a = s.start_appium()
    print a
