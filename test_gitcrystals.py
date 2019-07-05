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

    def test_display_location(self):
        game = GitCrystalsCmd()
        game.display_location()
        expected ="""You are in Mountain Gate
To your north is... Git Crystal
To your south is... 
To your east is... 
To your west is... 
"""
        self.assertEqual(game.output, expected)
        game.do_quit('')

    def test_display_wrong_location(self):
        game = GitCrystalsCmd()
        game.player.location = "Not a location"
        game.display_location()
        expected = "You are not in a room on the world map. Try altering your location via git. \n"
        self.assertEqual(game.output, expected)

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
