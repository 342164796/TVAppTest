# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import lib.Utils as U
import lib.Logging as L
import yaml
def get_device_name():
    """

    :return: 返回一个包含正在连接的设备名称
    """
    device_list = []
    for device in U.cmd('adb devices').stdout.readlines():
        if 'device' in device and 'devices' not in device:
            device = device.split('\t')[0]
            device_list.append(device)
    return device_list
def get_android_version(device):
    """

    :param device: devicename
    :return: 返回该设备的安卓版本号
    """
    for version in U.cmd('adb -s %s shell getprop' % device).stdout.readlines():
        if 'ro.build.version.release' in version:
            version = version.split(':')[1].strip().strip('[]')
            L.Logging.info('get device: %s, version: %s' % (device,version))
            return version

def get_device_detail():
    """

    :return:返回一个设备详细信息的字典 包含deviceName 和deviceversion
    """
    device_details=[]
    for device in get_device_name():
        device_detail={}
        device_detail['deviceName'] = device
        device_detail['platformVersion'] = get_android_version(device)
        device_details.append(device_detail)
    L.Logging.info('get device details:%s' % device_details)
    return device_details
def set_device_yaml():
    device_lst = get_device_detail()
    for device in device_lst:
        L.Logging.success('get device:{},Android Version:{}'.format(device['deviceName'],
                          device['platformVersion']))
    ini = U.ConfigIni()
    with open(ini.get_ini('test_device','device'),'w') as f:
        yaml.dump(device_lst,f)
        f.close()

def get_device_info():
    device_list = []
    ini = U.ConfigIni()
    test_info = ini.get_ini('test_info', 'info')
    test_device = ini.get_ini('test_device', 'device')
    with open(test_info) as f:
        test_dict = yaml.load(f)
    with open(test_device) as f:
        for device in yaml.load(f):
            device_list.append(dict(test_dict.items() + device.items()))
    return device_list
if __name__ == '__main__':
    print get_device_info()