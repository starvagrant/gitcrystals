#!/usr/bin/env python3

import cmd
import subprocess
import gitconstants as G
import command_wrapper as cw
from jsondata import JsonData
import character, worldmap


class GitCrystalsCmd(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self.output = ''
        self.error = ''
        json_files = []
        json_files.append(JsonData("game-repo","alive"))
        json_files.append(JsonData("game-repo","location"))
        json_files.append(JsonData("game-repo","inventory"))
        json_files.append(JsonData("game-repo","status"))
        self.player = character.Character(json_files)
        self.world_map = worldmap.WorldMap()

    def display_location(self):
        location = self.player.location
        room = self.world_map.rooms.data.get(location, None)
        if room is not None:
            print("You are in " + location)
            print("To your north is... " + self.world_map.get_direction(location, 'north'))
            print("To your south is... " + self.world_map.get_direction(location, 'south'))
            print("To your east is... " + self.world_map.get_direction(location, 'east'))
            print("To your west is... " + self.world_map.get_direction(location, 'west'))

    def display_output(self):
        print(self.output)

    def display_error(self):
        print(self.error)

    def do_print(self, args):
        print(args)

    def do_quit(self,args):
        return True

    def do_revlist(self, args):
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'rev-list', 'HEAD']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

    def do_branch(self, args):
        first_arg = args.split()[0] # do not allow branches with space names
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch', first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

        if len(args.split()) > 1:
            print('branch names cannot have spaces ' + first_arg + ' used as branch name')

    def do_listbranches(self, args):
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

    def do_checkout(self, args):
        first_arg = args.split()[0]
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'checkout', first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

    def do_checkoutfile(self, args):
        first_arg = args.split()[0]
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'checkout', '--',first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

    def do_stage(self, args):
        first_arg = args.split()[0]
        if first_arg.endswith('.json'):
            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'add', first_arg]
            process = cw.run_process(command)
            self.output = process.stdout
            self.error = process.stderr
        else:
            print("Type 1 file name exactly")
            print("Example: 'stage princess/location.json'")

    def do_unstage(self, args):
        first_arg = args.split()[0]
        if first_arg.endswith('.json'):
            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'reset','--mixed','HEAD', first_arg]
            process = cw.run_process(command)
            self.output = process.stdout
            self.error = process.stderr
        else:
            print("Type 1 file name exactly")
            print("Example: 'unstage princess/location.json'")

    def do_commit(self, args):
        if args == '':
            if self.player.alive == True:
                message = "Player is alive in " + self.player.location + "."
            else:
                message = "Player is dead in " + self.player.location + "."
        else:
            message = args
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'commit','-m', message]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

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
