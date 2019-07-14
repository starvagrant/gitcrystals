#!/usr/bin/env python3

from project.gitcrystals import GitCrystalsCmd
import project.gitglobals as G
import project.command_wrapper as cw
from project.jsondata import JsonData
from project.character import Character
import unittest
import subprocess
from collections import OrderedDict

class Tests(unittest.TestCase):

    # Test game quits correctly
    def test_do_quit(self):
        game = GitCrystalsCmd()
        self.assertTrue(game.do_quit(''))

    def test_display_location(self):
        game = GitCrystalsCmd()
        expected ="""You are in Mountain Gate
To your north is... Git Crystal
To your south is... 
To your east is... 
To your west is... 
"""
        self.assertEqual(game.display_location(), expected)
        game.do_quit('')

    def test_display_wrong_location(self):
        game = GitCrystalsCmd()
        game.player.location = "Not a location"
        expected = "You are not in a room on the world map. Try altering your location via git. \n"
        self.assertEqual(game.display_location(), expected)

    def test_display_ground(self):
        G.change_location_file("Git Crystal")

        game = GitCrystalsCmd()
        expected = "In Git Crystal you see...\n    Git Status Tutorial\n    Intro Git Tutorial\n"
        self.assertEqual(game.display_ground(), expected)

        G.change_location_file("Mountain Gate")

    def test_display_characters(self):
        G.change_location_file("Mountain Gate")

        game = GitCrystalsCmd()
        expected = 'There is no here but you\n'
        self.assertEqual(game.display_characters(), expected)

        G.change_location_file("Dragon's Lair")
        game = GitCrystalsCmd()
        expected = "In Dragon's Lair you see...\n    princess\n    grandfather\n    dragon\n"
        self.assertEqual(game.display_characters(), expected)

        G.change_location_file("Mountain Gate")

    def test_create_character(self):
        G.change_location_file("Mountain Gate")
        game = GitCrystalsCmd()
        player = game.player
        self.assertEqual(player.js_location.data['location'], "Mountain Gate")
        princess = game.create_character('princess')
        self.assertEqual(princess.js_location.data['location'], "Dragon's Lair")

    def test_go(self):
        G.change_location_file("Mountain Gate")
        game = GitCrystalsCmd()
        game.do_go('north')
        expected_location = "Git Crystal"
        player_location = game.player.location
        json_file = JsonData(G.repodir,"location")
        file_location = json_file.data['location']

        self.assertEqual(player_location, expected_location)
        self.assertEqual(file_location, expected_location)

        G.change_location_file("Mountain Gate")

    def test_do_look(self):
        G.change_location_file("Mountain Gate")
        game = GitCrystalsCmd()
        expected = """You are in Mountain Gate
To your north is... Git Crystal
To your south is... 
To your east is... 
To your west is... 
In Mountain Gate you see...
    No Trespassing Sign
There is no here but you
"""
        game.do_look('')
        self.assertEqual(game.output, expected)

        expected = """You are in Mountain Gate
To your north is... Git Crystal
To your south is... 
To your east is... 
To your west is... 
"""
        game.do_look('room')
        self.assertEqual(game.output, expected)

        expected = """In Mountain Gate you see...
    No Trespassing Sign
"""

        game.do_look('ground')
        self.assertEqual(game.output, expected)

        expected = """There is no here but you
"""
        game.do_look('people')
        self.assertEqual(game.output, expected)

    def test_do_take(self):
        game = GitCrystalsCmd()
        game.do_take('No Trespassing Sign')
        inventory_list = [("Basic Clothes",1),("Distress Note",1),("Git Gem",1),("No Trespassing Sign",1)]
        actual_inventory = game.player.js_inventory.data
        expected_inventory = OrderedDict(inventory_list)
        self.assertEqual(actual_inventory, expected_inventory)
        game.do_drop('No Trespassing Sign')

    def test_do_drop(self):
        game = GitCrystalsCmd()
        game.do_take('No Trespassing Sign')
        game.do_drop('No Trespassing Sign')
        actual_inventory = game.player.js_inventory.data
        inventory_list = [("Basic Clothes",1),("Distress Note",1),("Git Gem",1)]
        expected_inventory = OrderedDict(inventory_list)
        self.assertEqual(actual_inventory, expected_inventory)

if __name__ == '__main__':
    unittest.main()
