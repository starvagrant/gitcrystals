#!/usr/bin/env python3

import json
from collections import OrderedDict

class JsonData(object):
    """ Constructor Loads Jsonfile of POSIX OS """
    def __init__(self, dirName="game-repo", name="alive"):
        self.file = dirName + "/" + name + ".json"
        self.name = name
        with open(self.file, 'r') as f:
            text = f.read()
            self.data = json.loads(text, object_pairs_hook=OrderedDict)

    def load(self):
        with open(self.file, 'r') as f:
            text = f.read()
            self.data = json.loads(text, object_pairs_hook=OrderedDict)
        return self.data

    def write(self):
        with open(self.file, 'w') as f:
            f.write(json.dumps(self.data, sort_keys=True,
                               indent=4, separators=(',',':')))
            f.write('\n\n')
            f.close()

if __name__ == '__main__':
    pass
