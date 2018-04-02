# -*- coding:utf-8 -*-
from analyzelog import analyzelog
from getcase import get_all_case
import yaml
import os
import adb
import lib.Utils as U
class generatereport():
    def __init__(self,all_result_path,device):
        self.all_result_path = all_result_path
        self.device = device
        self.adb = adb.adb(self.device)
    def __analyze_log(self):
        a = analyzelog(self.all_result_path)
        a.main()
    def __yaml_file(self,all_result_path,extension_name):
        return get_all_case(all_result_path,extension_name)
    def __open_yaml(self,file_path):
        if file_path is None:
            return None
        with open(file_path) as f:
            y = yaml.load(f)
            return y['error_msg']
    def __confirm_file(self,file_path):
        if os.path.exists(file_path):
            return file_path
        else:
            return None
    def __app_info(self):
        ini = U.ConfigIni()
        package_name = ini.get_ini('test_package_name','packageName')
        app_version_name = self.adb.get_app_version(package_name)
        return package_name,app_version_name
    @U.log_flie_function()
    def __device_info(self):
        return 'device_name:' + str(self.adb.get_device_name()), \
               'disk:' + str(self.adb.get_disk()), \
               'wifi_name:' + str(self.adb.get_wifi_name()), \
               'system_version:' + str(self.adb.get_android_version()), \
               'resolution:' + str(self.adb.get_screen_resolution())
    @U.log_flie_function()
    def __test_case_execution_status(self):
        number_of_test_cases = self.__yaml_file(self.all_result_path,'.yaml').values()
        passed = 0
        failed = 0
        for i in number_of_test_cases:
            if isinstance(self.__open_yaml(i),bool):
                passed +=1
            else:
                failed +=1
        return len(number_of_test_cases),passed,failed
    def main(self):
        import GetHtml
        self.__analyze_log()
        result = self.__yaml_file(self.all_result_path,'.yaml')
        lst = []
        for case_name, confirm_status in result.items():
            case_name = str(case_name).split('.')[0]
            case_result = self.__open_yaml(confirm_status)
            case_img = self.__confirm_file(str(confirm_status).replace('status','img').replace('yaml','png'))
            case_per = self.__confirm_file(str(confirm_status).replace('status','per').replace('yaml','png'))
            case_log = self.__confirm_file(str(confirm_status).replace('status','log').replace('yaml','log'))
            case_filter = self.__confirm_file(str(confirm_status).replace('status','log').replace('yaml','log')
                                              .replace(case_name,case_name + 'filter'))
            if case_per is None:
                ini = U.ConfigIni()
                case_per = ini.get_ini('test_case','error_img')
            lst.append(
                GetHtml.get_html_tr(
                    case_name,
                    case_result,
                    case_img,
                    case_per,
                    case_log,
                    case_filter
                )
            )
        GetHtml.get_html(''.join(lst),
                         self.__app_info(),
                         self.__device_info(),
                         self.__test_case_execution_status(),
                         self.all_result_path)



