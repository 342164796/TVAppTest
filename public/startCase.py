# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from appium import webdriver
import public.getcase
import public.startAppium
import ExecuteCase
import lib.Logging as L
import lib.Utils as U
import time
import os
from public import clean
class run_case(object):
    def __init__(self,device_list):
        self.time = time.strftime(
            "%Y-%m-%d_%H_%M%S",
            time.localtime(
                time.time()
            )
        )
        self.device_list = device_list
        self.device = self.device_list['deviceName']
        L.Logging.info('start test device:%s' % self.device)
        self.all_result_path = self.mkdir_file()
 #       self.appium = self.start_appium()
    def mkdir_file(self):
        ini = U.ConfigIni()
        result_path = ini.get_ini('test_case','log_file')
        result_path_file = result_path + '\\' + self.time
        file_list = [
            result_path,
            result_path_file,
            result_path_file + '\log',
            result_path_file + '\per',
            result_path_file + '\img',
            result_path_file + '\status']
        if not os.path.exists(result_path):
            os.mkdir(result_path)
        for file_path in file_list:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        return result_path_file
    def __get_appium_port(self):
        sp = public.startAppium.startAppium(self.device)
        self.appium_port = sp.main()
        return self.appium_port
    def start_appium(self):
        try:
            self.driver = webdriver.Remote(
                'http://127.0.0.1:%s/wd/hub' %
                self.__get_appium_port(),self.device_list
            )
            L.Logging.debug('appium start %s success' % self.device)
            U.sleep(10)
            return self.driver
        except Exception as e:
            L.Logging.error('Failed to start appium : {}'.format(e))
            L.Logging.error(
                'Try restartting the appium:{}'.format(self.device,)
            )


    def run_case(self,yaml_name,yaml_path):
        run = ExecuteCase.start_case(
            self.start_appium(),
     #       self.appium,
            yaml_name,
            yaml_path,
            self.all_result_path,
            self.device
        )
        return run.main()
    def case_start(self):
        test_case_yaml = public.getcase.get_case_yaml_path().items()
        if not test_case_yaml:
            L.Logging.error('yaml not found!!!')
        else:
            for yaml_name,yaml_path in test_case_yaml:
                L.Logging.success('yaml path:{}'.format(yaml_path))
                self.run_case(yaml_name,yaml_path)
                try:
                    self.driver.quit()
                    L.Logging.success('quit driver %s' % self.appium_port)
                    U.sleep(5)
                except:
                    L.Logging.error('quit driver error %s' % self.appium_port)
                clean.clean_appium(self.appium_port,self.device)
if __name__ == '__main__':
    import public.getDevices
    public.getDevices.set_device_yaml()
    for device in public.getDevices.get_device_info():
        a = run_case(device)
        a.case_start()