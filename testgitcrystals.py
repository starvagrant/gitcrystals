#!/usr/bin/env python3

from gitcrystals import GitCrystalsCmd
import unittest
import subprocess
import gitconstants as G
import command_wrapper as cw

current_commit_sha='75f9ce255a19d4f4b347b679e00ebee2ad027046'
current_branch='data'

def test_clean_repo():
    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'rev-list', 'HEAD']
    process = cw.run_process(command)
    output = process.stdout
    if not output==current_commit_sha + '\n':
        print(output)
        print("Extra commits found in test repository, please reset")
        return False

    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'status', '--short']
    process = cw.run_process(command)
    output = process.stdout
    if not output=='':
        print("Working Directory or Index Not Clean. Please clear")
        return False

    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'show-ref', '--heads']
    process = cw.run_process(command)
    output = process.stdout
    lines = output.split('\n')
    if not lines[-1:]==['']: # last element will be empty string if only one ref
        print('Unnecessary Branches, Please Delete')
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

    def test_branch(self):
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_branch('newbranch')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch']
            process = cw.run_process(command)
            output = process.stdout

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch', '-d', 'newbranch']
            process = cw.run_process(command)

            expected = "* data\n  newbranch\n"
            self.assertEqual(output, expected)

unittest.main()
