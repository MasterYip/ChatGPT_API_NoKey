# ChatGPT_API_NoKey

[中文](README.md)|**English**


Screw the APIKEY! Chat to GPT with NO KEY!
## Features
ChatGPT_API_NoKey is a simple ChatGPT fake API that mimics keyboard and mouse operations, allowing users to interact with GPT without the need for an APIKEY.

**Note**:
1. For the first-time use, set `HEADLESS=False` and manually log in to ChatGPT to save cookies for automatic login in subsequent sessions. The script does not include any other listening functionalities, as assured by the author.
2. Abusing this API may lead to account issues, so please control the request frequency appropriately.
3. Currently, only single-thread blocking mode is supported, and concurrent request processing is still under development.

## Installation and Usage
1. Environment Setup

Please install **Google Chrome** first.
```
cd <work-dir>
pip install -r .\requirements.txt
```
2. Config Configuration

`HEADLESS`: Whether to run Chrome in headless mode. If set to True, Chrome will run in headless mode without displaying the browser window. If set to False, Chrome will run in normal mode and display the browser window. (**Note: There is a small bug in undetected_chromedriver when `HEADLESS=True`. The solution is provided in `example.py`.**)

`HEADER`: User-agent header for browser requests.

`SERVER_ADDRESS`: Server address and port number tuple for the FakeAPI.

`PROXY`: Proxy used to access ChatGPT. In this configuration, the proxy is set to None, indicating no proxy is used (or the system's default proxy) to access ChatGPT. If you need to use a proxy, you can set the proxy address to the corresponding string, such as "http://127.0.0.1:7890". Please ensure that the proxy is set correctly to ensure proper access to ChatGPT.

3. Quick Start (example.py includes relevant routines)

run example.py
```
python ./example.py
```

Direct Call to FakeAPI
```
api = FakeAPI(HEADLESS, PROXY, HEADER)
print(api.request("Hello!"))
```
Using as a Server
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

## Future Work
- Implement multi-threaded concurrent request processing based on Flask.

## Acknowledgements

Thanks to the following projects for their valuable contributions to this project:

- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

And other projects that may have been accidentally overlooked :)

Special thanks to the open-source community and all contributors for their contributions to this project.

## License
This project is released under the MIT license. For more information, please see the [LICENSE](LICENSE) file.

## Author
Master Yip

Email: 2205929492@qq.com

GitHub: [Master Yip](https://github.com/MasterYip)