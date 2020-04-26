CLIENT_PARAMS = {}
TOKEN = 'YOUR TOKEN HERE'
ADMINS = [55555555, 6666666] # user IDs with admin privileges, ID can be retrieved by sending the bot the command "what_is_my_id"
COMMAND_PREFIX = '$'
MODULES = [
    'manage',
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
