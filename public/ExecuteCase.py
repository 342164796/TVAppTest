# -*- coding: utf-8 -*-
import BasePage
import sys
sys.path.append('..')
import public.adb
import public.getcase
import lib.Logging as L
import lib.Utils as U
import yaml
import public.generatereport
import public.performance
reload(sys)
sys.setdefaultencoding("utf-8")
class BB(BasePage.Base):
    pass
class start_case():
    def __init__(self,driver,yaml_name,yaml_path,all_result_path,device):
        self.yaml_path = yaml_path
        self.filename = str(yaml_name).split('.')[0]
        self.driver = BB(driver)
        self.device = device
        self.all_result_path = all_result_path
    @U.log_flie_function()
    def __save_cpu_mem(self,cpu,mem,h_cpu,h_mem):
        per_img_file = self.all_result_path + '\per\{}.png'.format(self.filename)
        public.performance.data_marker(cpu,mem,h_cpu,h_mem,per_img_file)
        return per_img_file
    @U.log_flie_function()
    def get_device_log(self):
        device_log = public.adb.adb(self.device)
        log_file = self.all_result_path + '\\log\\{}.log'.format(self.filename)
        device_log.logcat_c()
        device_log.logcat(log_file)
        return log_file
    def get_all_case(self,yaml_path):
        def get_case(yaml_path):
            case_list=[]
            inherit_case_file = public.getcase.get_case_yaml_path()
            with open(yaml_path) as f:
                for case in yaml.load(f):
                    if isinstance(case,dict):
                        if 'test_inherit' in case:
                            inherit_case_name = case['test_inherit']
                            inherit_case = inherit_case_name + '.yaml'
                            if inherit_case in inherit_case_file.keys():
                                case_list += case_list + get_case(inherit_case_file[inherit_case])
                        else:
                            case_list.append(case)
                    else:
                        L.Logging.warn('get_case:not found')
            return case_list
        return get_case(yaml_path)
    def __select_per(self,case_name, device_name):
        sql = U.sql()
        return sql.select_per(case_name,device_name)
    def __save_sql(self,case_name,device_name,cpu_list,mem_list,execution_status):
        sql = U.sql()
        sql.insert_per(case_name,device_name,cpu_list,mem_list,execution_status)
        sql.close()
    @U.e()
    def analysis_yaml(self,yaml_path):
        adb = public.adb.adb(self.device)
        ini = U.ConfigIni()
        packageName = ini.get_ini('test_package_name','packageName')
        cpu_list = []
        mem_list = []
        for case in self.get_all_case(yaml_path):
            L.Logging.success('get case %s' % str(case))
            if isinstance(case,dict):
                if 'name' in case:
                    test_name = str(case['name']).decode('utf-8')
                    L.Logging.info('Start the test_case: {}'.format(test_name))
                test_range = 1
                if 'range' in case:
                    test_range = case['range']
                for i in xrange(0,test_range):
                    if case['action'] == 'click':
                        test_control_type = case['type']
                        test_control = case['element']
                        L.Logging.success('click {}'.format(test_control))
                        self.driver.clickButton(test_control_type,test_control)
 ######(继续写）                   elif case['test_action'] == 'send_keys'
                    elif case['action'] == 'find':
                        test_control_type = case['type']
                        test_control = case['element']
                        L.Logging.success('find {}'.format(test_control))
                        self.driver.find_element(test_control_type,test_control)
                    elif case['action'] == 'keyevent':
                        keys = case['keys']
                        self.driver.keyevent(keys)
                        if case.has_key('assert'):
                            verification = case['assert']
                            verifications = []
                            source = self.driver.assertion()
                            for v in verification.split(','):
                                if v:
                                    verifications.append(v)
                            print verifications
                            for ve in verifications:
                                try:
                                    assert source.find(ve) != -1
                                    L.Logging.success('assert {}'.format(ve))
                                except:
                                    raise Exception('not found %s in page!!!!' % ve)
                        elif case.has_key('or_assert'):
                            verification = case['or_assert']
                            source = self.driver.assertion()
                            for v in verification.split(','):
                                if v:
                                    verifications.append(v)
                            result = []
                            for ve in verifications:
                                re = source.find(ve)
                                result.append(re)
                            l = len(result)
                            if result.count('-1') == l:
                                raise Exception("can't find any element in %s page" % verification)
                    elif case['action'] == 'assert':
                        verifications = []
                        verification = case['element']
                        source = self.driver.assertion()
                        for v in verification.split(','):
                            if v:
                                verifications.append(v)
                        for ve in verifications:
                            assert source.find(ve) != -1
                            L.Logging.success('assert {}'.format(ve))
                    elif case['action'] == 'or_assert':
                        verifications = []
                        verification = case['verification']
                        source = self.driver.assertion()
                        for v in verification.split(','):
                            if v:
                                verifications.append(v)
                        result = []
                        for ve in verifications:
                            re = source.find(ve)
                            result.append(re)
                        for i in result:
                            if i != -1:
                                break
                            else:
                                continue
                            raise Exception('not found any element %s in page' % verification)
                    elif case['action'] == 'tap':
                        position = case['position']
                        self.driver.tap(position)
                    elif case['action'] == 'start_activity':
                        packageName = case['packageName']
                        activity = case['activity']
                        self.driver.start_activity(packageName,activity)

                    if 'sleep' in case:
                        sleep = case['sleep']
                        self.driver.sleep(int(sleep))


                    cpu = adb.get_cpu(packageName)
                    mem = adb.get_mem(packageName)
                    cpu_list.append(cpu)
                    mem_list.append(mem)
            else:
                L.Logging.error('Yaml file format error, the current {} , you need dict.'.format(type(case)))

        historical_per = self.__select_per(self.filename, self.device)
        self.__save_sql(self.filename, self.device, cpu_list, mem_list, 1)
        if historical_per is not None:
            h_cpu = historical_per[0]
            h_mem = historical_per[1]
            self.__save_cpu_mem(cpu_list,mem_list,h_cpu,h_mem)
        else:
            self.__save_cpu_mem(cpu_list,mem_list,None,None)
        L.Logging.success('cpu_list:{}'.format(cpu_list))
        L.Logging.success(('mem_list:{}'.format(mem_list)))
        return True



    @U.log_flie_function()
    def __save_error_status(self):
        error_file = self.all_result_path + '\status\{}.yaml'.format(self.filename)
        return error_file
    @U.log_flie_function()
    def __save_screen_file(self):
        screen_file = self.all_result_path + '\img\{}.png'.format(self.filename)
        try:
            self.driver.save_screenshot(screen_file)
        except:
            L.Logging.debug('Appium screenshot err, now use adb screenshot')
            adb = public.adb.adb(self.device)
            adb.get_sceenshot(screen_file)
        return screen_file
    @U.log_flie_function()
    def __save_android_reslut(self):
        r = public.generatereport.generatereport(self.all_result_path,self.device)
        r.main()
        return self.all_result_path
    def start_test(self):
        L.Logging.success('read the yaml file')
        self.get_device_log()
        error_msg = self.analysis_yaml(self.yaml_path)
        with open(self.__save_error_status(),'w') as f:
            yaml.dump({'error_msg': error_msg},f)
            L.Logging.debug(str('results of the : %s' % error_msg))
            f.close()
        return self.__save_screen_file()
    def main(self):
        U.sleep(5)
        self.start_test()
        U.sleep(2)
        self.__save_android_reslut()
