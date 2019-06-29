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

if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.cmdloop()
