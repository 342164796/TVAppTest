import subprocess
import time
import os
import sys
import ConfigParser
import Logging as L
import traceback
import sqlite3
import re
def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
def cmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
def sleep(s):
    return time.sleep(s)
class ConfigIni():
    def __init__(self):
        self.current_directory = os.path.split(os.path.realpath(sys.argv[0]))[0]
#        self.path = self.current_directory.replace('lib','data\\test_info.ini')
        self.path = 'E:\\TVAppTest\\data\\test_info.ini'
        self.cf = ConfigParser.ConfigParser()

        self.cf.read(self.path)

    def get_ini(self,title,value):
        return self.cf.get(title, value)
    def set_int(self,title,value,text):
        self.cf.set(title,value,text)
        return self.cf.write(open(self.path,'wb'))
    def add_ini(self,title):
        self.cf.add_section(title)
        return self.cf.write(open(self.path))
    def get_options(self,data):
        options = self.cf.options(data)
        return options
    def a(self):
        return self.get_ini('test_case','case')


def log_flie_function():
    def log(func):
        def wrapper(*args,**kwargs):
            t = func(*args, **kwargs)
            filename = str(sys.argv[0]).split('.')[0]
            L.Logging.success('{}:{}, return:{}'.format(filename, func.__name__, t))
            return t
        return wrapper
    return log
def e():
    def E(func):
        def wrapper(*args,**kwargs):
            error_msg = True
            try:
                return func(*args,**kwargs)
            except AssertionError as e:
                L.Logging.warn(traceback.format_exc())
                L.Logging.error(e)
                error_msg = 'Assertion error'
            except AttributeError as e:
                L.Logging.warn(traceback.format_exc())
                L.Logging.error(e)
                error_msg = 'Attribute Error'
            except Exception as e:
                error_msg = traceback.format_exc()
                L.Logging.error(e)
            finally:
                return error_msg
        return wrapper
    return E
class sql:
    def __init__(self):
        ini = ConfigIni()
        db_path = ini.get_ini('test_db','test_result')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__is_table()
    def __is_table(self):
        self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='test_results'")
        row = self.cursor.fetchone()
        if row[0] !=1:
            self.__built_table()
    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
    def __built_table(self):
        self.cursor.execute("""
        CREATE TABLE test_results
        (
            case_id INTEGER PRIMARY KEY,
            case_name TEXT,
            device_name TEXT,
            cpu_list TEXT,
            mem_list TEXT,
            execution_status TEXT,
            create_time DATETIME DEFAULT (datetime('now','localtime'))
        );
        """)
    def select_per(self,case_name,device_name):
        statement = "select * from test_results where " \
                    "case_name = '{}' " \
                    "and " \
                    "device_name = '{}' " \
                    "and " \
                    "execution_status = 1 " \
                    "order by create_time desc".format(case_name,device_name)
        self.cursor.execute(statement)
        row = self.cursor.fetchone()
        if row is not None:
            cpu = re.findall(r"\d+\.?\d*", row[3])
            mem = re.findall(r"\d+\.?\d*", row[4])
            return [int(i) for i in cpu], [int(i) for i in mem]
        else:
            return None
    def insert_per(self, case_name, device_name, cpu_list, mem_list, execution_status):
        key = "(case_name,device_name,cpu_list,mem_list,execution_status,create_time)"
        values = "('{}','{}','{}','{}','{}','{}')".format(case_name,device_name,cpu_list,mem_list,execution_status,
                                                          get_now_time())
        self.cursor.execute("INSERT INTO test_results {} VALUES {}".format(key,values))



if __name__ =='__main__':
    a = sql()
    print a.select_per('login','192.168.1.100:5555')
