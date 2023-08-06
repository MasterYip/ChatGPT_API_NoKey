import os
import logging

HEADLESS = True
HEADER = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
# PROXY = None
PROXY = "http://127.0.0.1:7890"  # If global proxy is set, you can leave it as None
# SERVER_ADDRESS = ('127.0.0.1',5000)
SERVER_ADDRESS = ('', 5000)
THEAD_NUM = 1

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
# Remove existing handlers for basicConfig to take effect.
# TODO: This may not be a good idea, because this will infect other modules.
root_logger = logging.getLogger()
for h in root_logger.handlers:
    root_logger.removeHandler(h)
logging.basicConfig(filename=os.path.join(ROOT_DIR, 'log.txt'),
                    format=format_str,
                    datefmt=datefmt_str,
                    level=logging.INFO)
cil_handler = logging.StreamHandler(os.sys.stderr)  # 默认是sys.stderr
cil_handler.setLevel(logging.INFO)  # TODO: 会被BasicConfig限制？(过滤树)
cil_handler.setFormatter(logging.Formatter(
    fmt=format_str, datefmt=datefmt_str))