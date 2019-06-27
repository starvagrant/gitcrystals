#!/usr/bin/env python3

import cmd
import subprocess
import gitconstants as G
import command_wrapper as cw

class GitCrystalsCmd(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self.output = ''
        self.error = ''

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


if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.cmdloop()
