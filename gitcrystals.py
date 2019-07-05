#!/usr/bin/env python3

import cmd,re
import subprocess
import gitconstants as G
import command_wrapper as cw
from jsondata import JsonData
import character, worldmap
import gitcli

class GitCrystalsCmd(gitcli.GitCmd):

    def __init__(self, repodir="game-repo"):
        super().__init__()
        self.output = ''
        self.error = ''
        self.repodir = repodir
        json_files = []
        json_files.append(JsonData("game-repo","alive"))
        json_files.append(JsonData("game-repo","location"))
        json_files.append(JsonData("game-repo","inventory"))
        json_files.append(JsonData("game-repo","status"))
        self.player = character.Character(json_files)
        self.world_map = worldmap.WorldMap()

    def display_location(self):
        self.output = ''
        location = self.player.location
        room = self.world_map.rooms.data.get(location, None)
        if room is not None:
            self.output += "You are in " + location + '\n'
            self.output += "To your north is... " + self.world_map.get_direction(location, 'north') + '\n'
            self.output += "To your south is... " + self.world_map.get_direction(location, 'south') + '\n'
            self.output += "To your east is... " + self.world_map.get_direction(location, 'east') + '\n'
            self.output += "To your west is... " + self.world_map.get_direction(location, 'west') + '\n'
        else:
            self.output += "You are not in a room on the world map. Try altering your location via git. \n"
        self.display_output()

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

if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.display_location()
    game.cmdloop()
