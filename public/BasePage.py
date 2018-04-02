# -*- coding:utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import sys
sys.path.append('..')
import lib.Logging as L
import lib.Utils as U
import exceptions
class Base():
    def __init__(self,appium_driver):
        self.driver = appium_driver
    def find_element_by_id(self,loc,wait = 15):
        try:
            WebDriverWait(self.driver, wait).until(
                lambda driver: driver.find_element_by_id(loc).is_displayed()
            )
            return self.driver.find_element_by_id(loc)
        except:
            L.Logging.error(u"%s 页面中未能找到 %s 元素" %(self,loc))
            raise Exception('can\'t find id : %s' % loc)
    def find_element_by_android_uiautomator(self,loc,wait = 15):
        try:
            WebDriverWait(self.driver,wait).until(
                lambda driver: driver.find_element_by_android_uiautomator("text(\"%s\")" % loc).is_displayed()
            )
            return self.driver.find_element_by_android_uiautomator("text(\"%s\")" % loc)
        except:
            L.Logging.error(u"%s 页面中未能找到 %s 元素" %(self,loc))
            raise Exception('can\'t find text: %s' % loc)
    def find_element_by_class_name(self,loc,wait = 15):
        try:
            WebDriverWait(self.driver,wait).until(
                lambda driver: driver.find_element_by_class_name(loc).is_displayed()
            )
            return self.driver.find_element_by_class_name(loc)
        except:
            L.Logging.error(u"%s 页面中未能找到 %s 元素" % loc)
            raise Exception('can not find class_name: %s' % loc)
    def clickButton(self,type,loc,find_first=True):
        if type == 'id':
            if find_first:
                self.find_element_by_id(loc)
            self.find_element_by_id(loc).click()
        elif type == 'text':
            if find_first:
                self.find_element_by_android_uiautomator(loc)
            self.find_element_by_android_uiautomator(loc).click()
    def sleep(self,time):
        L.Logging.success("begin sleep {}s".format(time))
        U.sleep(time)
    def keyevent(self,key):
        key_dict = {'up':19,'down':20,'left':21,'right':22,'ok':23,'back':111}
        keys = key.split(',')
        for key in keys:
            L.Logging.success("keyevent {}".format(key_dict[key]))
            self.driver.keyevent(key_dict[key])
            U.sleep(1)
    def assertion(self):
        source = self.driver.page_source
        return source
    def find_element(self,type,loc):
        if type == 'id':
            self.find_element_by_id(loc)
        elif type == 'text':
                self.find_element_by_android_uiautomator(loc)
    def save_screenshot(self, file_path):
        return self.driver.get_screenshot_as_file(file_path)
    def start_activity(self,package,activity):
        return self.driver.start_activity(package,activity)
    def tap(self,position):
        position = position.split(',')
        return self.driver.tap(position)