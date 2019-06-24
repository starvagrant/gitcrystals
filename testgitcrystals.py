#!/usr/bin/env python3

from gitcrystals import GitCrystalsCmd
import unittest

first_commit_sha='75f9ce255a19d4f4b347b679e00ebee2ad027046'

class Tests(unittest.TestCase):

    # Test game quits correctly
    def test_do_quit(self):
        game = GitCrystalsCmd()
        self.assertTrue(game.do_quit(''))

    def test_do_revlist(self):
        game = GitCrystalsCmd()
        self.assertEqual(game.do_revlist(''), first_commit_sha)

unittest.main()
