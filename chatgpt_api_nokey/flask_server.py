'''
Author: MasterYip 2205929492@qq.com
Date: 2023-08-06 14:43:20
LastEditors: MasterYip
LastEditTime: 2023-08-06 15:58:40
FilePath: \ChatGPT_API_NoKey\chatgpt_api_nokey\flask_server.py
Description: file content
'''

from .config import *
from .fake_api import MultiThreadedFakeAPI, FakeAPI

from flask import Flask, request
from multiprocessing import cpu_count, Process
from gevent import monkey
from gevent.pywsgi import WSGIServer
# monkey.patch_all()
import json

# Flask
app = Flask(__name__)
multiServer = None
# api = MultiThreadedFakeAPI()
api = FakeAPI()

# 创建POST请求处理的路由
@app.route('/post', methods=['POST'])
def handle_post_request():
    data = request.json
    return api.request(json.dumps(data))

def server_forever():
    multiServer.start_accepting()
    multiServer._stop_event.wait()
    
def launchFlaskServer(address=SERVER_ADDRESS):
    global multiServer
    multiServer = WSGIServer(address, app)
    multiServer.start()
    for i in range(2):
        print("Starting process " + str(i) + "...")
        p = Process(target=server_forever)
        p.start()

class FlaskServer(object):

    def __init__(self, threadNum=THEAD_NUM, headless=HEADLESS, proxy=PROXY, header=HEADER, server_address=SERVER_ADDRESS):
        self.logger = logging.getLogger('FlaskServer')
        self.logger.addHandler(cil_handler)
        self.address = server_address
        self.api = MultiThreadedFakeAPI(
            threadNum=threadNum, headless=headless, proxy=proxy, header=header)
        self.launchFlaskServer()

    def launchFlaskServer(self):
        global multiServer
        multiServer = WSGIServer(self.address, app)
        multiServer.start()
        self.multiServer = multiServer
        global api
        api = self.api
        for i in range(cpu_count()):
            print("Starting process " + str(i) + "...")
            p = Process(target=server_forever)
            p.start()


