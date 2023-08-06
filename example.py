'''
Author: MasterYip 2205929492@qq.com
Date: 2023-08-06 16:31:07
LastEditors: MasterYip
LastEditTime: 2023-08-06 20:47:10
FilePath: \ChatGPT_API_NoKey\example.py
Description: file content
'''
import time
import openai
from threading import Thread
from chatgpt_api_nokey.fake_api import FakeAPI
from chatgpt_api_nokey.singlethread_server import SingleThreadServer

# CONFIG (default values are set in chatgpt_api_nokey/config.py)
HEADLESS = False                     # Whether to run Chrome in headless mode
"""
Note: There is a bug in undetected-chromedriver when setting headless=True.
For short term, you can modify the source code of undetected-chromedriver in `__init__.py`
385        if headless or options.headless:
387            # FIXME: uc version_main is > 108
388            if not self.patcher.version_main:
389                self.patcher.version_main = 110
390            if self.patcher.version_main < 108:
391                options.add_argument("--headless=chrome")
392            elif self.patcher.version_main >= 108:
393                options.add_argument("--headless=new")
"""
HEADER = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) \
    AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
SERVER_ADDRESS = ('', 5000)         # Server address (i.e. openai.api_base="http://localhost:5000")
PROXY = None                        # Proxy used to access ChatGPT
# PROXY = "http://127.0.0.1:7890"   # If global proxy is set, you can leave it as None


def FakeAPIExample():
    api = FakeAPI(HEADLESS, PROXY, HEADER)
    print(api.request("Hello!"))


def SingleThreadServerExample():
    Thread(target=SingleThreadServer, args=(HEADLESS, PROXY, HEADER, SERVER_ADDRESS)).start()
    time.sleep(20)  # Wait for the server to start (It's better to start the server in another thread)
    openai.api_base = "http://localhost:5000"
    openai.api_key = "whatever"
    completions = openai.ChatCompletion.create(
                        model="whatever",
                        messages="Hello!",
                    )
    print(completions['choices'][0]['message']['content'])
    completions = openai.ChatCompletion.create(
                        model="whatever",
                        messages="How to write a program that can get rid of the APIKEY?",
                    )
    print(completions['choices'][0]['message']['content'])


if __name__ == "__main__":
    FakeAPIExample()
    # SingleThreadServerExample()
