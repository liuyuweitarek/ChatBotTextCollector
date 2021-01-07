"""
File: server.py
Author: YUWEI LIU
Institution:  Modeling and Informatics Laboratory
Version: v0.1.0
"""
from selenium import webdriver
import os, time, rpyc, argparse,random,re
from fake_useragent import UserAgent

def execute_script(driver, xpath):
    """ wrapper for selenium driver execute_script
    :param driver: selenium driver
    :param xpath: (str) xpath to the element
    :return:  execute_script result
    """
    execute_string = "window.document.evaluate('{}', document, null, 9, null).singleNodeValue.click();".format(xpath)

    return driver.execute_script(execute_string)

class WooServer(object):
    def __init__(self, args):
        # Connect to rpyc server
        self.conn = rpyc.connect("localhost", port=args.W_rpyc_port, config=rpyc.core.protocol.DEFAULT_CONFIG)
        self.parent = self.conn.root
        self.parent.server_close(False)
        
        self.options = webdriver.ChromeOptions()
        ua = UserAgent()
        userAgent = ua.random
        # Load Server Parameters
        #self.path = os.path.dirname(os.path.abspath(__file__)) + '/'
        # self.vpn = VPN('/mnt/c/c/Users/User/AppData/Local/Google/Chrome/User Data/Default/Extensions/gjknjjomckknofjidppipffbpoekiipm/6.4.4_0.crx')
        # self.options = self.vpn.options
        self.options.add_argument(f'user-agent={userAgent}')
        self.driver = webdriver.Chrome('./' + args.W_webdriver_type + 'driver.exe',chrome_options=self.options)
        self.driver.implicitly_wait(30)
        self.base_url = args.W_base_url
        # self.bot = ElizaBot()
        self.bot = PandoraBot(user_id=random.randint(1,1e7))

    def start(self):
        # self.vpn.switch(self.driver)
        self.driver.get(self.base_url)
        time.sleep(random.randint(2,5))
        self.driver.find_element_by_id("open-left").click()
        execute_script(self.driver,"/html/body/div[5]/div/ul[1]/li[1]/a")
        time.sleep(random.randint(2,5))
        self.driver.find_element_by_id("keyInput").clear()
        self.driver.find_element_by_id("keyInput").send_keys("測試")
        time.sleep(random.randint(2,5))
        self.driver.find_element_by_id("startButton").click()
        message_sent = False
        reply = None
        hisreply = ""
        msg = u'女'
        i = 0
        while True:
            print("進到迴圈")
            sysText = self.driver.find_elements_by_xpath("//div[@class=\"system text \"]")
            strangerText = self.driver.find_elements_by_xpath("//div[@class=\"stranger text \"]")
            if strangerText:
                print("有")
                reply = re.findall(".*陌生人：(.*?)\s.*",strangerText[-1].text)[0]
                if reply:
                    print("有Reply")
            if len(sysText) == 1 and "請開啟此連結" in [info.text for info in sysText][0]:
                print("等驗證")
                self.parent.server_close(True)

            elif (len(sysText)==2 or len(sysText)==4 or len(sysText)==6 or len(sysText)==8) and (hisreply != reply):
                print("進到對話")
                self.driver.find_element_by_id("messageInput").clear()
                if reply:
                    botreply = self.bot.query(reply)
                    botreply.replace("This bot is being leeched from w w w . k u k i . b o t (no spaces) - Please visit there to talk to the real version of the bot and do not support the leechers.This bot is being leeched from w w w . k u k i . b o t (no spaces) - Please visit there to talk to the real version of the bot and do not support the leechers.", "")
                    self.driver.find_element_by_id("messageInput").send_keys(botreply)
                else:
                    self.driver.find_element_by_id("messageInput").send_keys(msg)
                time.sleep(random.randint(1,3))
                self.driver.find_element_by_css_selector("#sendButton > input[value=\"傳送\"]").click()
                self.driver.find_element_by_xpath("//div[@class=\"me text\"]")
                i = 0
                message_sent = True
                hisreply = reply

            elif (len(sysText)==5 or len(sysText)==7 or len(sysText)==9):
                print('對方離開')
                time.sleep(random.randint(2,5))
                self.driver.find_element_by_css_selector("#changeButton > input[value=\"離開\"]").click()
                time.sleep(random.randint(2,5))
                self.driver.find_element_by_id("startButton").click()
                i = 0
                message_sent = False

            else:
                 print(i)
                 time.sleep(1)
                 i += 1
                 if i == 30:
                    print('超過時間,換人!')
                    self.driver.find_element_by_css_selector("#changeButton > input[value=\"離開\"]").click()
                    self.driver.find_element_by_id("popup-yes").click()
                    time.sleep(1)
                    self.driver.find_element_by_id("startButton").click()
                    i = 0
                    message_sent = False
                 



            # Signal WooServer is ready to main thread
            if not self.parent.server_ready():
                self.parent.server_ready(True)  

            # Close window when signaled by main thread
            if self.parent.server_close():
                self.close()
                break


    def close(self):
        self.parent.server_ready(False)
        self.vpn.switch(self.driver)
        self.driver.close()
        return

if __name__ == "__main__":
    from vpn import VPN
    from eliza import ElizaBot
    from mitsuku import PandoraBot
    # Load Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--W_rpyc_port', type=int, default=12345, help='Default:12345 \n Description:RPYC Service PORT need to be int 10000-65535')
    parser.add_argument('--W_webdriver_type', type=str, default='chrome', help='Support types: chrome')
    parser.add_argument('--W_base_url', type=str, default='https:\/\/wootalk.today', help='Support URLS: \"https:\/\/wootalk.today\"')
    args = parser.parse_args() 

    # Launch Server

    wServer = WooServer(args)

    wServer.start()
