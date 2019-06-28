#!/usr/bin/env python3

from gitcrystals import GitCrystalsCmd
import unittest
import subprocess
import gitconstants as G
import command_wrapper as cw


current_commit_sha='280affe6f75332425b216cb163e5b8c3ec14ef58'
current_branch='data'

def test_clean_repo():
    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'rev-list', 'HEAD']
    process = cw.run_process(command)
    output = process.stdout
    if not output.split('\n')[0]==current_commit_sha:
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
            head_commit = game.output.split('\n')[0]
            self.assertEqual(head_commit, current_commit_sha)

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

    def test_listbranches(self):
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_listbranches('')

            expected = "* data\n"
            self.assertEqual(game.output, expected)

    def test_checkout_same_ref(self):
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_branch('newbranch')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'checkout','newbranch']
            process = cw.run_process(command)

            game.do_checkout('newbranch')
            game.do_listbranches('')
            expected = "  data\n* newbranch\n"
            actual = game.output

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'checkout',current_branch]
            process = cw.run_process(command)
            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch', '-d', 'newbranch']
            process = cw.run_process(command)

            self.assertEqual(actual, expected)

    def test_checkout_file(self):
        if test_clean_repo():

            game = GitCrystalsCmd()
            with open('game-repo/README.md', 'a') as f:
                f.write("##Test Header")

            game.do_checkoutfile('README.md')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'status','--short']
            process = cw.run_process(command)

            expected = ''
            self.assertEqual(process.stdout, expected)

unittest.main()
