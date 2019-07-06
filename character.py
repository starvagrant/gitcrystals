#!/usr/bin/env python3

import jsondata

class Character():

    def __init__(self, json_files, name="player"):
        self.js_relationship = None
        self.name = name
        for json_file in json_files:
            if json_file.name == "alive":
                self.js_alive = json_file
            if json_file.name == "status":
                self.js_status = json_file
            if json_file.name == "inventory":
                self.js_inventory = json_file
            if json_file.name == "location":
                self.js_location = json_file
            if json_file.name == "relationship":
                self.js_relationship = json_file

        if self.js_relationship is None:
            self.is_player = True
        else:
            self.is_player = False

        self.alive = self.js_alive.data['alive']
        self.location = self.js_location.data['location']
