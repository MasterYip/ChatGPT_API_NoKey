'''
Author: MasterYip 2205929492@qq.com
Date: 2023-08-06 14:58:29
LastEditors: MasterYip
LastEditTime: 2023-08-06 15:31:06
FilePath: \ChatGPT_API_NoKey\test.py
Description: file content
'''
from chatgpt_api_nokey.singlethread_server import SingleThreadServer
from chatgpt_api_nokey.flask_server import FlaskServer, launchFlaskServer

launchFlaskServer()
# server = FlaskServer() 
# print([i for i in range(1)])