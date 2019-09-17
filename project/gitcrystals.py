#!/usr/bin/env python3

import cmd,re
import subprocess
from collections import OrderedDict
import project.gitglobals as G
import project.command_wrapper as cw
from project.jsondata import JsonData
from project.character import Character
from project.worldmap import WorldMap
import project.gitcli as gitcli

class GitCrystalsCmd(gitcli.GitCmd):
    prompt = '\n\033[32mGit Crystals>\033[0m'

    def __init__(self, repodir="game-repo"):
        super().__init__(repodir)
        self.output = ''
        self.error = ''
        self.repodir = repodir
        self.load_data()

    def postcmd(self, stop, line):
        self.write_data()
        self.load_data()
        return stop

    def do_checkoutfile(self, args):
        player_is_alive = super().do_checkoutfile(args)
        self.load_data()
        if not player_is_alive:
            return True

    def do_checkout(self, args):
        player_is_alive = super().do_checkout(args)
        self.load_data()
        if not player_is_alive:
            return True

    def do_checkoutforce(self, args):
        player_is_alive = super().do_checkoutforce(args)
        self.load_data()
        if not player_is_alive:
            return True

    def do_merge(self, args):
        player_is_alive = super().do_merge(args)
        self.load_data()
        if not player_is_alive:
            return True

    def do_resolveleft(self, args):
        player_is_alive = super().do_resolveleft(args)
        self.load_data()
        if not player_is_alive:
            return True

    def do_resolveright(self, args):
        player_is_alive = super().do_resolveright(args)
        self.load_data()
        if not player_is_alive:
            return True

    def create_character(self, char_name):
        json_files = []
        data_folder = self.repodir + '/' + char_name
        json_files.append(JsonData(data_folder,"alive"))
        json_files.append(JsonData(data_folder,"location"))
        json_files.append(JsonData(data_folder,"inventory"))
        json_files.append(JsonData(data_folder,"status"))
        json_files.append(JsonData(data_folder,"relationship"))
        return Character(json_files, char_name)

    def load_data(self):
        json_files = []
        json_files.append(JsonData(self.repodir,"alive"))
        json_files.append(JsonData(self.repodir,"location"))
        json_files.append(JsonData(self.repodir,"inventory"))
        json_files.append(JsonData(self.repodir,"status"))
        self.player = Character(json_files)
        self.world_map = WorldMap(self.repodir,"world_rooms")
        self.characters = OrderedDict()
        self.characters['princess'] = self.create_character('princess')
        self.characters['grandfather'] = self.create_character('grandfather')
        self.characters['dragon'] = self.create_character('dragon')
        self.characters['shopkeeper'] = self.create_character('shopkeeper')

    def write_data(self):
        self.player.js_alive.write()
        self.player.js_location.write()
        self.player.js_inventory.write()
        self.player.js_status.write()
        self.world_map.rooms.write()
        for char in self.characters:
            self.characters[char].js_alive.write()
            self.characters[char].js_location.write()
            self.characters[char].js_inventory.write()
            self.characters[char].js_status.write()
            self.characters[char].js_relationship.write()

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
            output = 'There is no here but you.\n'
        else:
            output = 'In ' + location + ' you see...\n' + characters_output
        return output

    def display_inventory(self):
        output = 'You have: \n'
        for item in self.player.js_inventory.data:
            output += str(self.player.js_inventory.data[item]) + ' of ' + item + '\n'
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
                self.output = "You are in " + self.player.location + '\n'
            else:
                self.output = "There's Nothing in that Direction"
        else:
            self.output = args + " is not a valid direction name"
        self.display_output()

    def do_east(self, args):
        self.do_go('east')

    def do_west(self, args):
        self.do_go('west')

    def do_north(self, args):
        self.do_go('north')

    def do_south(self, args):
        self.do_go('south')

    def do_search(self, args):
        self.output = self.display_ground()
        self.display_output()
        location = self.player.location
        if 'danger_search' in self.world_map.rooms.data[location]:
            self.player.js_alive.data['alive'] = False
            status = self.world_map.rooms.data[location]['danger_search']
            self.player.js_status.data[status] = True
            for char in self.characters:
                if self.characters[char].js_location.data['location'] == location:
                    self.characters[char].js_alive.data['alive'] = False
                    self.characters[char].js_status.data[status] = True
            return True
        else:
            return False

    def do_take(self, args):
        self.output = ''
        location = self.player.location
        ground_items = self.world_map.get_ground_items(location)
        if args in ground_items.keys():
            ground_items[args] -= 1
            if args in self.player.js_inventory.data.keys():
                self.player.js_inventory.data[args] += 1
            else:
                self.player.js_inventory.data[args] = 1
            if ground_items[args] <= 0:
                ground_items.pop(args)
            self.world_map.set_ground_items(location, ground_items)
            self.output += 'Added ' + args + ' to player inventory'
        else:
            self.output += 'No ' + args + ' in ' + location + '\n'
            self.output += 'Inspect ground and type name exactly' + '\n'
        self.display_output()

    def do_drop(self, args):
        self.output = ''
        location = self.player.location
        ground_items = self.world_map.get_ground_items(location)
        if args in self.player.js_inventory.data:
            if args in ground_items:
                ground_items[args] += 1
            else:
                ground_items[args] = 1
            self.player.js_inventory.data[args] -= 1
            if self.player.js_inventory.data[args] <= 0:
                self.player.js_inventory.data.pop(args)

            self.world_map.set_ground_items(location, ground_items)
            self.output += "Dropped " + args + " in " + location + '\n'
        else:
            self.output += "You do not have " + args + "in your inventory" + '\n'
            self.output += "Type 'look inventory' to see what items you have" + '\n'

        self.display_output()

    def do_look(self, args):
        self.output = ''
        if args == '':
            self.output += self.display_location()
            self.output += self.display_characters()
        elif args.lower() == 'room':
            self.output += self.display_location()
        elif args.lower() == 'people':
            self.output += self.display_characters()
        elif args.lower() == 'inventory':
            self.output += self.display_inventory()
        else:
            self.output += "Examples: 'look', 'look room', 'look people, look inventory'"

        self.display_output()

if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.display_location()
    game.cmdloop()
