import os
import logging
import simplejson as json

log = logging.getLogger(__name__)

class JSONDatabase:
    def __init__(self, path, default=dict):
        '''' default can also be a function '''
        self.path = path
        if os.path.exists(path):
            with open(path) as f:
                self.data = json.load(f)
        else:
            if callable(default):
                self.data = default()
            else:
                self.data = default

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
