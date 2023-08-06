# ChatGPT_API_NoKey

**中文**|[English](README_en.md)

去他的APIKEY！调用没有APIKEY的ChatGPT！

Screw the APIKEY! Chat to GPT with NO KEY!

## 功能介绍

ChatGPT_API_NoKey通过模仿键鼠操作实现简单的ChatGPT fake API，以方便广大穷苦百姓免遭APIKEY的毒害。

**注意**：
1. 首次使用时，应设置HEADLESS=False，手动登录ChatGPT，登陆后保存cookie便于后续自动登录。（作者用头承诺脚本中不包含其他监听信息的功能）
2. 滥用此API可能导致账号异常，请适当控制请求频率。
3. 目前仅支持单线程阻塞模式，并发请求处理仍然在开发当中。

## 安装使用
1. 环境配置
```
cd <work-dir>
pip install -r .\requirements.txt
```
2. Config配置

`HEADLESS`：是否在无头模式下运行Chrome浏览器。如果设置为True，将以无头模式运行Chrome浏览器，不会显示浏览器窗口。如果设置为False，将以普通模式运行Chrome浏览器，会显示浏览器窗口。（**注意，undetected_chromedriver在HEADLESS=True时存在小bug, 解决方式在example.py中给出**）

`HEADER`：浏览器请求的用户代理头。

`SERVER_ADDRESS`：FakeAPI服务器的地址和端口号元组。

`PROXY`：访问ChatGPT的代理。在这个配置中，代理设置为None，表示不使用代理（或系统默认代理）来访问ChatGPT。如果你需要使用代理，可以将代理地址设置为对应的字符串，如"http://127.0.0.1:7890"。请确保代理设置正确，以确保能够正确地访问ChatGPT。

3. 开箱使用（example.py包含相关例程）

FakeAPI直接调用
```
api = FakeAPI(HEADLESS, PROXY, HEADER)
print(api.request("Hello!"))
```
作为Server使用
```
Thread(target=SingleThreadServer, args=(HEADLESS, PROXY, HEADER, SERVER_ADDRESS)).start()
time.sleep(15)  # Wait for the server to start (It's better to start the server in another thread)
openai.api_base = "http://localhost:5000"
openai.api_key = "whatever"
completions = openai.ChatCompletion.create(
                    model="whatever",
                    messages="Hello!",
                )
print(completions['choices'][0]['message']['content'])
```
## 未来工作
- 基于Flask多线程并发请求处理

## 鸣谢

感谢以下项目对本项目的宝贵贡献：

- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

以及其他不小心被忽略的项目 :)

特别感谢开源社区和所有为该项目作出贡献的贡献者。

## 许可证
本项目在MIT许可下发布。有关详细信息，请参阅[LICENSE](LICENSE)文件。

## 作者
Master Yip

电子邮件：2205929492@qq.com

GitHub：[Master Yip](https://github.com/MasterYip)