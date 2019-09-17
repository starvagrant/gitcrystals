#!/usr/bin/env python3

import cmd,re
import subprocess
import project.gitglobals as G
import project.command_wrapper as cw
from project.jsondata import JsonData

class GitCmd(cmd.Cmd):
    prompt = '\n\033[31m Git Mode>\033[0m '

    def __init__(self, repodir="game-repo"):
        super().__init__()
        self.output = ''
        self.error = ''
        self.repodir = repodir
        self.alive = JsonData(self.repodir,"alive")

    def is_player_alive(self):
        self.alive.load()
        if self.alive.data['alive'] == True:
            return True
        else:
            return False

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

    def do_quit(self,args):
        return True

    def do_revlist(self, args):
        command = [G.GIT, '-C', self.repodir, 'rev-list', 'HEAD']
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
        command = [G.GIT,'--no-pager','-C',self.repodir,'log', entries, '--decorate']
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
        command = [G.GIT,'--no-pager','-C',self.repodir,'log', entries,'--oneline','--decorate','--graph','--all']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr
        print(self.output)

    def do_branch(self, args):
        first_arg = args.split()[0] # do not allow branches with space names
        command = [G.GIT, '-C', self.repodir, 'branch', first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

        if len(args.split()) > 1:
            print('branch names cannot have spaces ' + first_arg + ' used as branch name')

    def do_listbranches(self, args):
        command = [G.GIT, '-C', self.repodir, 'branch']
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr
        self.display_output()

    def do_checkout(self, args):
        first_arg = args.split()[0]
        command = [G.GIT, '-C', self.repodir, 'checkout', first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

        return self.is_player_alive()

    def do_checkoutfile(self, args):
        first_arg = args.split()[0]
        command = [G.GIT, '-C', self.repodir, 'checkout', '--',first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

        return self.is_player_alive()

    def do_checkoutforce(self,args):
        first_arg = args.split()[0]
        command = [G.GIT, '-C', self.repodir, 'checkout', '-f',first_arg]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

        return self.is_player_alive()

    def do_stage(self, args):
        first_arg = args.split()[0]
        if first_arg.endswith('.json'):
            command = [G.GIT, '-C', self.repodir, 'add', first_arg]
            process = cw.run_process(command)
            self.output = process.stdout
            self.error = process.stderr
        else:
            print("Type 1 file name exactly")
            print("Example: 'stage princess/location.json'")

    def do_unstage(self, args):
        first_arg = args.split()[0]
        if first_arg.endswith('.json'):
            command = [G.GIT, '-C', self.repodir, 'reset','--mixed','HEAD', first_arg]
            process = cw.run_process(command)
            self.output = process.stdout
            self.error = process.stderr
        else:
            print("Type 1 file name exactly")
            print("Example: 'unstage princess/location.json'")

    def do_commit(self, args):
        message = args
        command = [G.GIT, '-C', self.repodir, 'commit','-m', message]
        process = cw.run_process(command)
        self.output = process.stdout
        self.error = process.stderr

    def do_status(self, args):
        command = [G.GIT,'-C', self.repodir,'status','--short']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diff(self, args):
        command = [G.GIT,'-C', self.repodir,'diff']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diffstaged(self, args):
        command = [G.GIT,'-C', self.repodir,'diff', '--cached']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diffchanges(self, args):
        command = [G.GIT,'-C', self.repodir,'diff', 'HEAD']
        process = cw.run_process(command)
        self.output = self.format_status(process.stdout)
        self.error = process.stderr
        self.display_output()

    def do_diffbranch(self, args):
        branches = []
        args = args.split()
        while(len(args) < 2):
            args.append('')
        command = [G.GIT,'-C', self.repodir,'show-ref', '--heads']
        process = cw.run_process(command)
        output = process.stdout
        output_lines = output.split('\n')
        if '' in output_lines:
            output_lines.pop()
        for line in output_lines:
            branches.append(re.sub(r'[0-9a-f]{40} refs/heads/','', line))

        if args[0] in branches and args[1] in branches:
            command = [G.GIT,'-C', self.repodir,'diff', args[0], args[1]]
            process = cw.run_process(command)
            self.output = process.stdout
        else:
            self.output = "only " + ",".join(branches) + " are legal branch names\n"
            self.output += "usage: diffbranch branch1 branch2\n"
        self.display_output()

    def do_merge(self, args):
        branches = []
        command = [G.GIT,'-C', self.repodir,'show-ref', '--heads']
        process = cw.run_process(command)
        output = process.stdout
        output_lines = output.split('\n')
        if '' in output_lines:
            output_lines.pop()
        for line in output_lines:
            branches.append(re.sub(r'[0-9a-f]{40} refs/heads/','', line))

        args = args.split()
        if len(args) == 1 and args[0] in branches:
            command = [G.GIT,'-C', self.repodir,'merge', '--no-ff','--log','-m','merge branch ' + args[0], args[0]]
            process = cw.run_process(command)
            self.output = process.stdout
            self.err = process.stderr
        elif len(args) == 0:
            self.output = "No branch names provided"
        elif len(args) > 1:
            self.output = "Git Crystals does not support merging mulitple branches"

        self.display_output()

        return self.is_player_alive()

    def do_resolveleft(self,args):
        args.split()
        for arg in args:
            command = [G.GIT,'-C', self.repodir,'checkout', '--ours', arg]
            process = cw.run_process(command)
            self.output = process.stdout
            self.err = process.stderr
            self.display_output()

        return self.is_player_alive()

    def do_resolveright(self,args):
        args.split()
        for arg in args:
            command = [G.GIT,'-C', self.repodir,'checkout', '--theirs', arg]
            process = cw.run_process(command)
            self.output = process.stdout
            self.err = process.stderr
            self.display_output()

        return self.is_player_alive()

if __name__ == '__main__':
    game = GitCrystalsCmd()
    game.display_location()
    game.cmdloop()
