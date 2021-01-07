"""
File: vpn.py
Author: YUWEI LIU
Institution:  Modeling and Informatics Laboratory
Version: v0.1.0
"""
from selenium import webdriver
import os, time
 
class VPN:
    def __init__(self, chrome_path):
        self.options = webdriver.ChromeOptions()
        self.prefs = {
            'profile.default_content_setting_values':
            {
                'notifications': 2
            }
        }

        #Google擴充套件的檔案位置
        self.options.add_extension(chrome_path)
        #將擴充套件放入至Webdriver的開啟網頁內容
        self.options.add_experimental_option('prefs', self.prefs)
        #隱藏『Chrome正在受到自動軟體的控制』這項資訊
        self.options.add_argument("disable-infobars")

    def switch(self,driver):
        driver.get("chrome-extension://gjknjjomckknofjidppipffbpoekiipm/panel/index.html")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="screenMain"]/div[3]/div[1]').click()
        time.sleep(1)