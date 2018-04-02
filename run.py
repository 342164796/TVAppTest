# -*- coding: utf-8 -*-
import public.startAppium
import public.getDevices
import public.startCase
import lib.Logging as L
import time
from multiprocessing import Process
import public.clean

import time
threads = []
def runCase(device):
    run = public.startCase.run_case(device)
    run.case_start()
def run_test():
    public.clean.clean_device_yaml()
    public.getDevices.set_device_yaml()
    device_list = public.getDevices.get_device_info()
    if len(device_list) == 0:
        L.Logging.error('devices is null')
    for device in device_list:
        t = Process(target=runCase ,args=(device,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
if __name__ == '__main__':
    run_test()

