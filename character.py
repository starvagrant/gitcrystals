#!/usr/bin/env python3

import jsondata

class Character():

    def __init__(self, json_files):
        self.data = {}
        for json_file in json_files:
            if json_file.name == "alive":
                self.data['alive'] = json_file.data
            if json_file.name == "status":
                self.data['status'] = json_file.data
            if json_file.name == "inventory":
                self.data['inventory'] = json_file.data
            if json_file.name == "location":
                self.data['location'] = json_file.data
            if json_file.name == "relationship":
                self.data['relationship'] = json_file.data

        if not 'relationship' in self.data:
            self.is_player = True
        else:
            self.is_player = False

        self.alive = self.data['alive']['alive']
        self.location = self.data['location']['location']
