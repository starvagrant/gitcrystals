#!/usr/bin/env python3

from gitcrystals import GitCrystalsCmd
import unittest
import subprocess
import gitconstants as G
import command_wrapper as cw
from jsondata import JsonData

repodir="game-repo"

class Tests(unittest.TestCase):

    # Test game quits correctly
    def test_do_quit(self):
        game = GitCrystalsCmd()
        self.assertTrue(game.do_quit(''))

    def test_go(self):
        game = GitCrystalsCmd()
        game.do_go('north')
        expected_location = "Git Crystal"
        player_location = game.player.location
        json_file = JsonData(repodir,"location")
        file_location = json_file.data['location']

        self.assertEqual(player_location, expected_location)
        self.assertEqual(file_location, expected_location)

        game.do_go('south')

unittest.main()
