#!/usr/bin/env python3

import cmd
import subprocess

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
        command = ['git', '--git-dir=game-repo/.git', '--work-tree=./game-repo', 'rev-list', 'first-commit']
        process = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output = process.stdout
        self.error = process.stderr

if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.cmdloop()
