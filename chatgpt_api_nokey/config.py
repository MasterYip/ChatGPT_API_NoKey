import os
import logging

# CONFIG
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
THEAD_NUM = 1                       # Thread number of the server

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()

COOKIES_FILE = os.path.join(ROOT_DIR, 'cookies.json')
TMP_SNAP_FILE = os.path.join(ROOT_DIR, 'tmp_snap.png')


# Logger
format_str = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(funcName)s - %(message)s'
datefmt_str = "%y-%m-%d %H:%M:%S"
root_logger = logging.getLogger()
# Remove existing handlers for basicConfig to take effect.
for h in root_logger.handlers:
    root_logger.removeHandler(h)
logging.basicConfig(filename=os.path.join(ROOT_DIR, 'log.txt'),
                    format=format_str,
                    datefmt=datefmt_str,
                    level=logging.INFO)
cil_handler = logging.StreamHandler(os.sys.stderr)
cil_handler.setLevel(logging.INFO)
cil_handler.setFormatter(logging.Formatter(
    fmt=format_str, datefmt=datefmt_str))
