CLIENT_PARAMS = {}
TOKEN = 'YOUR TOKEN HERE'
COMMAND_PREFIX = '$'
MODULES = [
    'example',
]

# logging

import sys
import logging
log = logging.getLogger('bot')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
