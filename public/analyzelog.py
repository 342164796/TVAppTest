# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
import lib.Utils as U
import public.getcase
import os
class analyzelog:
    def __init__(self,all_result_path):
        self.all_result_path = all_result_path
    @U.log_flie_function()
    def __log_file(self,all_result_path,extension_name):
        return public.getcase.get_all_case(all_result_path,extension_name).values()
    def analyze(self,log_file):
        errorId = 0
        go_on_id = 0
        log_filter_name = os.path.split(log_file)[1].split('.')[0]
        with open(self.all_result_path + '\\log\\{}filter.log'.format(log_filter_name),'w') as s:
            with open(log_file) as f:
                for line in f:
                    if 'Exception' in line:
                        go_on_id =1
                        s.write('#' + '-' * 40 + '/n')
                        s.write(line)
                        errorId = line.split('(')[1].split(')')[0].strip()
                    elif go_on_id ==1:
                        if errorId in line:
                            s.write(line)
                        else:
                            go_on_id = 0
    def main(self):
        for logfile in self.__log_file(self.all_result_path,'.log'):
            self.analyze(logfile)