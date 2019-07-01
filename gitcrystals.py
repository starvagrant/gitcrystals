#!/usr/bin/env python3

import cmd,re
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

    def format_status(self, text):
        lines = text.split('\n')
        status_lines = []
        for line in lines:
            if line.startswith('M',0):
                status_lines.append(re.sub(r'^.{3}', '    staged changes: ', line))
            if line.startswith('M',1):
                status_lines.append(re.sub(r'^.{3}', '    unstaged changes: ', line))
            if not line.startswith('M',0) and not line.startswith('M',1):
                status_lines.append(line)

        if "\n".join(status_lines) == '':
            return("No changes since last commit\n")
        return "\n".join(status_lines)

    def do_print(self, args):
        print(args)

    def do_quit(self,args):
        return True

    def do_revlist(self, args):
        command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'rev-list', 'HEAD']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

    def do_log(self, args):
        if args.split() != []:
            arg = args.split()[0]
        else:
            arg = 4
        try:
            entries = int(arg)
        except ValueError:
            entries = 4
        entries = '-' + str(entries)
        command = ['git','--no-pager','-C','game-repo','log', entries, '--decorate']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr
        print(self.output)

    def do_graph(self, args):
        if args.split() != []:
            arg = args.split()[0]
        else:
            arg = 20
        try:
            entries = int(arg)
        except ValueError:
            entries = 20
        entries = '-' + str(entries)
        command = ['git','--no-pager','-C','game-repo','log', entries,'--oneline','--decorate','--graph','--all']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr
        print(self.output)

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
        self.display_output()

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

    def do_status(self, args):
        command = ['git','-C', 'game-repo','status','--short']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diff(self, args):
        command = ['git','-C', 'game-repo','diff']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diffstaged(self, args):
        command = ['git','-C', 'game-repo','diff', '--cached']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diffchanges(self, args):
        command = ['git','-C', 'game-repo','diff', 'HEAD']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diffbranch(self, args):
        branches = []
        args = args.split()
        while(len(args) < 2):
            args.append('')
        command = ['git','-C', 'game-repo','show-ref', '--heads']
        process = cw.run_process(command)
        output = process.stdout
        output_lines = output.split('\n')
        if '' in output_lines:
            output_lines.pop()
        for line in output_lines:
            branches.append(re.sub(r'[0-9a-f]{40} refs/heads/','', line))

        if args[0] in branches and args[1] in branches:
            command = ['git','-C', 'game-repo','diff', args[0], args[1]]
            process = cw.run_process(command)
            self.output = process.stdout
        else:
            self.output = "only " + ",".join(branches) + " are legal branch names\n"
            self.output += "usage: diffbranch branch1 branch2\n"
        self.display_output()

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
