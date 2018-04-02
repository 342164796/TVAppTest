# -*- coding: utf-8 -*-
import time
def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
class Logging:
    flag = True
    @staticmethod
    def error(msg):
        if Logging.flag == True:
            colour.show_error(get_now_time() + " [Error]:" + ''.join(msg))
    @staticmethod
    def warn(msg):
        if Logging.flag ==True:
            colour.show_warn(get_now_time() + " [Warn]:" + ''.join(msg))
    @staticmethod
    def info(msg):
        if Logging.flag == True:
            colour.show_info(get_now_time() + " [Info]:" + ''.join(msg))
    @staticmethod
    def debug(msg):
        if Logging.flag == True:
            colour.show_debug(get_now_time() + " [Debug]:" + ''.join(msg))
    @staticmethod
    def success(msg):
        if Logging.flag ==True:
            colour.show_verbose(get_now_time() + " [Success]:" + ''.join(msg))
class colour:
    @staticmethod
    def c(msg,colour):
        try:
            from termcolor import colored, cprint
            p = lambda x: cprint(x, '%s' % colour)
            return p(msg)
        except:
            print msg
    @staticmethod
    def show_verbose(msg):
        colour.c(msg, 'white')
    @staticmethod
    def show_debug(msg):
        colour.c(msg, 'blue')
    @staticmethod
    def show_info(msg):
        colour.c(msg,'green')
    @staticmethod
    def show_warn(msg):
        colour.c(msg,'yellow')
    @staticmethod
    def show_error(msg):
        colour.c(msg,'red')


