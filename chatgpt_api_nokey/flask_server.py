from threading import Thread
from flask import Flask, request, jsonify
from multiprocessing import cpu_count, Process
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()

# Flask
flaskServer = Flask(__name__)
multiThreadApi = None


# 创建POST请求处理的路由
@flaskServer.route('/post', methods=['POST'])
def handle_post_request():
    data = request.json
    multiThreadApi.request(json.dumps(data))
    return "Post request received and being processed."


def launchFlaskServer(multiApi, address=SERVER_ADDRESS):
    mulserver = WSGIServer(address, flaskServer)
    mulserver.start()
    global multiThreadApi
    multiThreadApi = multiApi

    def server_forever():
        mulserver.start_accepting()
        mulserver._stop_event.wait()

    for i in range(cpu_count()):
        p = Process(target=server_forever)
        p.start()