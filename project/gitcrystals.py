#!/usr/bin/env python3

import cmd,re
import subprocess
from collections import OrderedDict
import project.gitconstants as G
import project.command_wrapper as cw
from project.jsondata import JsonData
from project.character import Character
from project.worldmap import WorldMap
import project.gitcli as gitcli

class GitCrystalsCmd(gitcli.GitCmd):

    def __init__(self, repodir="game-repo"):
        super().__init__()
        self.output = ''
        self.error = ''
        self.repodir = repodir
        json_files = []
        json_files.append(JsonData(repodir,"alive"))
        json_files.append(JsonData(repodir,"location"))
        json_files.append(JsonData(repodir,"inventory"))
        json_files.append(JsonData(repodir,"status"))
        self.player = Character(json_files)
        self.world_map = WorldMap()
        self.characters = OrderedDict()
        self.characters['princess'] = self.create_character('princess')
        self.characters['grandfather'] = self.create_character('grandfather')
        self.characters['dragon'] = self.create_character('dragon')
        self.characters['shopkeeper'] = self.create_character('shopkeeper')

    def create_character(self, char_name):
        json_files = []
        data_folder = self.repodir + '/' + char_name
        json_files.append(JsonData(data_folder,"alive"))
        json_files.append(JsonData(data_folder,"location"))
        json_files.append(JsonData(data_folder,"inventory"))
        json_files.append(JsonData(data_folder,"status"))
        json_files.append(JsonData(data_folder,"relationship"))
        return Character(json_files, char_name)

    def display_location(self):
        output = ''
        location = self.player.location
        room = self.world_map.rooms.data.get(location, None)
        if room is not None:
            output += "You are in " + location + '\n'
            output += "To your north is... " + self.world_map.get_direction(location, 'north') + '\n'
            output += "To your south is... " + self.world_map.get_direction(location, 'south') + '\n'
            output += "To your east is... " + self.world_map.get_direction(location, 'east') + '\n'
            output += "To your west is... " + self.world_map.get_direction(location, 'west') + '\n'
        else:
            output += "You are not in a room on the world map. Try altering your location via git. \n"
        return output

    def display_ground(self):
        output = ''
        location = self.player.location
        room = self.world_map.rooms.data.get(location, None)
        if room is not None:
            ground_items = self.world_map.get_ground_items(location)
            if ground_items == []:
                output += 'The ground is empty' + '\n'
            else:
                output += 'In ' + location + ' you see...' + '\n'
                for item in ground_items:
                    output += '    ' + item + '\n'
        else:
            output = "You are not in a room on the world map. Try altering your location via git. \n"
        return output

    def display_characters(self):
        output = ''
        characters_output = ''
        location = self.player.location
        room = self.world_map.rooms.data.get(location, None)
        if room is not None:
            for key in self.characters:
                if self.characters[key].location == location:
                    characters_output += '    ' + self.characters[key].name + '\n'
        if characters_output == '':
            output = 'There is no here but you\n'
        else:
            output = 'In ' + location + ' you see...\n' + characters_output
        return output

    def display_output(self):
        print(self.output)

    def display_error(self):
        print(self.error)

    def do_print(self, args):
        print(args)

    def do_quit(self,args):
        return True

    def do_go(self, args):
        direction = args.lower()
        if direction in ['north','south','east','west']:
            location = self.player.location
            new_location = self.world_map.get_direction(location, direction)
            if new_location != '':
                self.player.location = new_location
                self.player.js_location.data['location'] = new_location
                self.player.js_location.write()
                self.display_location()
            else:
                print("There's Nothing in that Direction")
        else:
            print(args + " is not a valid direction name")

    def do_east(self, args):
        self.do_go('east')

    def do_west(self, args):
        self.do_go('west')

    def do_north(self, args):
        self.do_go('north')

    def do_south(self, args):
        self.do_go('south')

    def do_take(self, args):
        self.output = ''
        location = self.player.location
        ground_items = self.world_map.get_ground_items(location)
        if args in ground_items:
           new_item = ground_items.pop(ground_items.index(args))
           self.player.js_inventory.data['items'].append(new_item)
           self.player.js_inventory.write()
           self.world_map.set_ground_items(location, ground_items)
           self.world_map.rooms.write()
           self.output += 'Added ' + args + ' to player inventory'
        else:
           self.output += 'No ' + args + ' in ' + 'location' + '\n'
           self.output += 'Inspect ground and type name exactly' + '\n'
        self.display_output()

    def do_look(self, args):
        self.output = ''
        if args == '':
            self.output += self.display_location()
            self.output += self.display_ground()
            self.output += self.display_characters()
        elif args.lower() == 'room':
            self.output += self.display_location()
        elif args.lower() == 'ground':
            self.output += self.display_ground()
        elif args.lower() == 'people':
            self.output += self.display_characters()
        else:
            self.output += "Examples: 'look', 'look room', 'look ground', 'look people'"

        self.display_output()

if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.display_location()
    game.cmdloop()
