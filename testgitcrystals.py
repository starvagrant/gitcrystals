#!/usr/bin/env python3

from gitcrystals import GitCrystalsCmd
import unittest
import subprocess

current_commit_sha='75f9ce255a19d4f4b347b679e00ebee2ad027046'

def test_clean_repo():
    command = ['git', '--git-dir=game-repo/.git', '--work-tree=./game-repo', 'rev-list', 'HEAD']
    process = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout
    if not output==current_commit_sha + '\n':
        print(output)
        print("Extra commits found in test repository, please reset")
        return False

    command = ['git', '--git-dir=game-repo/.git', '--work-tree=./game-repo', 'status', '--short']
    process = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout
    if not output=='':
        print("Working Directory or Index Not Clean. Please clear")
        return False

    return True

class Tests(unittest.TestCase):

    # Test game quits correctly
    def test_do_quit(self):
        game = GitCrystalsCmd()
        self.assertTrue(game.do_quit(''))

    def test_do_revlist(self):
        if test_clean_repo():
            game = GitCrystalsCmd()
            game.do_revlist('')
            self.assertEqual(game.output, current_commit_sha + '\n')

    def test_command_syntax(self):
        commands = [['git checkout branchname', ['git','checkout','branchname']],
                    ['git checkout branchname file filename',['git','checkout','branchname','--','filename']],
                    ['git checkout file filename',['git','checkout','HEAD','--','filename']],
                    ['git force checkout branchname',['git checkout -f branchname']],
                    ['git checkout new branch branchname',['git checkout -b branchname']],
                    ['git branch delete branchname',['git','branch','-d','branchname']],
                    ['git force delete branchname', ['git','branch','-d', 'branchname']],
                    ['git log short',['git','log','--oneline']],
                    ['git log graph',['git','log','--oneline','--decorate','--graph','--all']],
                    ['git log',['git', 'log']],
                    ['git log diffs',['git','log','-p']],
                    ['git diff unstaged',['git','diff']],
                    ['git diff staged',['git', 'diff', '--cached']],
                    ['git diff uncommitted',['git','diff','HEAD']],
                    ['git diff unstaged branchname',['git','diff','branchname']],
                    ['git diff staged branchname',['git', 'diff', '--cached', 'branchname']],
                    ['git status',['git','status']],
                    ['git merge branchname prefer current',['git','merge','branchname','--strategy=recursive','--strategy-option=ours']],
                    ['git merge branchname prefer changes',['git','merge','branchname','--strategy=recursive','--strategy-option=theirs']]]

        game = GitCrystalsCmd()
        for command in commands:
            game.do_git(command[0][4:])
            self.assertListEqual(game.gitcommand, command[1])

    def test_branch(self):
        if test_clean_repo():
            command = ['git', '--git-dir=game-repo/.git', '--work-tree=./game-repo', 'branch', 'newbranch']
            process = subprocess.run(command)

            command = ['git', '--git-dir=game-repo/.git', '--work-tree=./game-repo', 'branch']
            process = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout
            error = process.stderr

            expected = "* data\nnewbranch\n"

            game = GitCrystalsCmd()
            game.do_branch('newbranch')
            self.assertEqual(game.output, expected)

            command = ['git', '--git-dir=game-repo/.git', '--work-tree=./game-repo', 'branch','-d', 'newbranch']
            process = subprocess.run(command)

unittest.main()
