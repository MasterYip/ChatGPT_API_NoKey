'''
Author: MasterYip 2205929492@qq.com
Date: 2023-08-06 14:45:50
LastEditors: MasterYip
LastEditTime: 2023-08-06 15:27:38
FilePath: \ChatGPT_API_NoKey\chatgpt_api_nokey\singlethread_server.py
Description: file content
'''

from .config import *
from .fake_api import FakeAPI

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, fakeapi, *args, **kwargs):
        self.logger = logging.getLogger('RequestHandler')
        self.logger.addHandler(cil_handler)
        self.api = fakeapi
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # 获取请求的内容长度
        content_length = int(self.headers['Content-Length'])
        # 读取请求的内容
        post_data = self.rfile.read(content_length)

        # 将请求的JSON数据转换为Python字典
        data = json.loads(post_data)
        chatText = json.dumps(data)
        self.logger.info("Req Received")
        response = self.api.request(chatText)

        # 处理请求数据（这里可以根据你的需求做相应处理）
        response = {
            "id": "chatcmpl-abc123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "fake-gpt-3.5-turbo",
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            },
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ]
        }
        response_json = json.dumps(response)

        # 设置响应头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # 发送响应数据
        self.wfile.write(response_json.encode())


class SingleThreadServer(object):

    def __init__(self, headless=HEADLESS, proxy=PROXY, header=HEADER, server_address=SERVER_ADDRESS):
        self.logger = logging.getLogger('SingleThreadServer')
        self.logger.addHandler(cil_handler)
        self.address = server_address
        self.api = FakeAPI(headless=headless, proxy=proxy, header=header)
        self.launchHTTPServer()

    def launchHTTPServer(self):
        self.server = HTTPServer(self.address,
                                 lambda *args, **kwargs: RequestHandler(self.api, *args, **kwargs))
        if self.address[0] == '':
            self.logger.info(
                f'Server is running on http://localhost:{self.address[1]}')
        else:
            self.logger.info(
                f'Server is running on http://{self.address[0]}:{self.address[1]}')
        self.server.serve_forever()
