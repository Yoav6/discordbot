CLIENT_PARAMS = {}
TOKEN = 'YOUR TOKEN HERE'
ADMINS = [55555555, 6666666] # user IDs with admin privileges, ID can be retrieved by sending the bot the command "what_is_my_id"
COMMAND_PREFIX = '$'
MODULES = [
    'manage',
    'example',
    'invites',
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

# invites module
INVITE_JOIN_TIME_REQUIREMENT = 60 * 60 * 24 * 40 # joined the guild >40 days ago
INVITE_JOIN_TIME_REQUIREMENT_READABLE = '40 days'
INVITE_QUOTA = (1, 60 * 60 * 24 * 7) # one invite per week
INVITE_QUOTA_HISTORY = 60 * 60 * 24 * 30 # number of seconds to save quota history (in case INVITE_QUOTA changes)
INVITE_MAX_AGE = 60 * 60 * 24 * 1 # duration of invite in seconds before expiry, or 0 for never. should be less than or equal to 86400
INVITE_MAX_USES = 1 # max number of uses or 0 for unlimited
INVITE_DB_PATH = 'invites.json'
