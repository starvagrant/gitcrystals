#!/usr/bin/env python3

import jsondata

class Data():
    def __init__(self):
        self.name = None
        self.status = None
        self.alive = None
        self.location = None
        self.relationship = None

class Character():

    def __init__(self, json_files):
        self.data = Data()
        for json_file in json_files:
            if json_file.name == "alive":
                self.data.alive = json_file.data
            if json_file.name == "status":
                self.data.status = json_file.data
            if json_file.name == "inventory":
                self.data.alive = json_file.data
            if json_file.name == "location":
                self.data.alive = json_file.data
            if json_file.name == "relationship":
               self.data.relationship = json_file.data

        if not self.data.relationship:
            self.is_player = True
        else:
            self.is_player = False
