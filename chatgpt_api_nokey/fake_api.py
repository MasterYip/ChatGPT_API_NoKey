'''
Author: MasterYip 2205929492@qq.com
Date: 2023-07-13 16:41:24
LastEditors: MasterYip
LastEditTime: 2023-08-12 20:05:44
FilePath: \ChatGPT_API_NoKey\chatgpt_api_nokey\fake_api.py
Description: file content
'''

from .config import *

import time
import json
import html2text
# import tiktoken
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def stringTokenNum(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

class FakeAPI(object):

    def __init__(self, headless=HEADLESS, proxy=PROXY, header=HEADER):
        self.logger = logging.getLogger('FakeAPI')
        self.logger.addHandler(cil_handler)
        self.url = 'https://chat.openai.com/'

        # Configure the Chrome options
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument(
            f"--user-agent={header}")
        chrome_options.add_argument("--enable-javascript")
        if proxy:
            chrome_options.add_argument(
                f'--proxy-server={proxy}')  # Default: follow system
        if headless:
            chrome_options.add_argument('--headless')
        # Launch the Chrome browser with proxy settings
        self.driver = uc.Chrome(options=chrome_options)
        self.logger.info('Server Initialized.')
        self.loginGPT()
        self.logger.info('Login Succeeded.')
        self.available = True

    # Launch
    def loginGPT(self):
        self.driver.get(self.url)
        self.driver.delete_all_cookies()
        if os.path.isfile(COOKIES_FILE):
            cookies = json.load(open(COOKIES_FILE, 'r'))
            # cookies = json.load(open(COOKIES_FILE, 'r'), encoding='utf-8')
            # 方法1 将expiry类型变为int
            for cookie in cookies:
                # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                if cookie.get('name') == '__Host-next-auth.csrf-token':
                    continue
                self.driver.add_cookie(cookie)
            self.driver.get(self.url)
            self.skipHint()
        else:
            input('Please login and press Enter to continue...\nIf HEADLESS is True, please set it to False for the first time.')
            self.saveCookies()

    def skipHint(self):
        hintFlag = True
        while hintFlag:
            buttons = self.getButtons()
            for button in buttons:
                if button.text == 'Next':
                    button.click()
                    break
                elif button.text == 'Done':
                    button.click()
                    hintFlag = False
                    break

    def saveCookies(self):
        cookies = self.driver.get_cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=4, ensure_ascii=False)

    # Extract
    def getContent(self):
        raw_content = self.driver.page_source
        # Format html content
        return BeautifulSoup(raw_content, 'html.parser').prettify()

    def getButtons(self):
        # return self.driver.find_element(by='css selector', value='button')
        # return self.driver.find_element(by=By.XPATH, value="//button[contains(@class, 'btn-neutral')]")
        # This works
        return self.driver.find_elements(by=By.CLASS_NAME, value="btn")

    def getTextInput(self):
        areas = self.driver.find_elements(by=By.TAG_NAME, value="textarea")
        while len(areas) == 0:
            self.logger.warning('No textarea found, refreshing...')
            self.driver.refresh()
            # time.sleep(0.2)
            areas = self.driver.find_elements(by=By.TAG_NAME, value="textarea")
        return areas[0]

    # FIXME: Answer mismatched
    def getLatestAnswer(self):
        """Get the latest answer from the answer divs."""
        ans = self.getAnswerDivs(toJson=True)
        if ans:
            # 将HTML富文本转换为Markdown
            return html2text.HTML2Text().handle(ans[-1])

    def getAnswerDivs(self, toJson=False):
        xpath = "//div[contains(@class, 'markdown prose w-full break-words dark:prose-invert light')]"
        elements = self.driver.find_elements(by=By.XPATH, value=xpath)
        if toJson:
            return [BeautifulSoup(element.get_attribute('innerHTML'), 'html.parser').prettify() for element in elements]
        else:
            return elements

    # Server
    def wait(self, timeout=20, poll_frequency=0.05):
        # self.driver.implicitly_wait(timeout)
        xpath = "//div[contains(@class, 'result-streaming')]"
        # Wait result-streaming div to disappear
        wait1 = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
        wait2 = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
        try:
            wait1.until(EC.presence_of_element_located((By.XPATH, xpath)))
            wait2.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
            return True
        except:
            return False

    def refresh(self, timeout=20):
        self.driver.refresh()
        # wait for the page to load
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
            return True
        except:
            self.logger.warning('Refresh failed...')
            return False

    def request(self, chatText, refreshlimit=7):
        """Send a request to the server and return the answer.
        
        """
        self.available = False
        flag = False
        textInput = self.getTextInput()
        textInput.send_keys(chatText)
        textInput.submit()
        while not flag:
            if self.wait():
                flag = True
                break
            else:
                self.logger.warning('Wait timeout, refreshing...')
                self.refresh()
            textInput = self.getTextInput()
            textInput.send_keys(chatText)
            textInput.submit()
            time.sleep(0.2)
        answer = self.getLatestAnswer()
        if len(self.getAnswerDivs()) > refreshlimit:
            self.logger.info('Webpage answer limit reached, refreshing...')
            self.refresh()
        self.available = True
        return answer

    def quit(self):
        self.driver.quit()

    def isAvailable(self):
        return self.available

    # Debugging
    def printElementInfo(self, webElement, showsnap=True):
        print('tag_name:', webElement.tag_name)
        print('text:', webElement.text)
        print('location:', webElement.location)
        print('size:', webElement.size)
        print('id:', webElement.id)
        print('rect:', webElement.rect)
        if showsnap:
            webElement.screenshot(TMP_SNAP_FILE)
            os.startfile(TMP_SNAP_FILE)


class MultiThreadedFakeAPI(object):

    def __init__(self, threadNum=THEAD_NUM, headless=HEADLESS, proxy=PROXY, header=HEADER):
        self.logger = logging.getLogger('MultiThreadedFakeAPI')
        self.logger.addHandler(cil_handler)
        self.logger.info(
            'Initializing MultiThreadedFakeAPI(probably time-consuming)...')
        self.apis = [FakeAPI(headless=headless, proxy=proxy,
                             header=header) for i in range(threadNum)]

    def request(self, chatText):
        while True:
            for api in self.apis:
                if api.isAvailable():
                    return api.request(chatText)
            time.sleep(0.1)



