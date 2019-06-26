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

unittest.main()
