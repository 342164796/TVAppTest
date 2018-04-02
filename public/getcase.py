# -*- coding: utf-8 -*-
import sys
sys.path.append(('..'))
import lib.Utils as U
import os
@U.log_flie_function()
def get_case_yaml_path():
    ini = U.ConfigIni()
    yaml_path = ini.get_ini('test_case','case')
    return get_all_case(yaml_path,'.yaml')

def get_all_case(directory,extension_name):
    file_dict = {}
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if 'filter' not in filename:
                if filename.endswith(extension_name):
                    path = os.path.join(parent,filename)
                    file_dict[filename] = path
    return file_dict

if __name__ == '__main__':
    a = get_case_yaml_path()
    print type(a)
