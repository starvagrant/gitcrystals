#!/usr/bin/env python3

from project.gitcrystals import GitCrystalsCmd
import project.gitconstants as G
import project.command_wrapper as cw
from project.jsondata import JsonData
from project.character import Character
import unittest
import subprocess

repodir="game-repo"

def change_location_file(new_location):
    json_file = JsonData(repodir,"location")
    json_file.data['location'] = new_location
    json_file.write()

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
        change_location_file("Git Crystal")

        game = GitCrystalsCmd()
        expected = "In Git Crystal you see...\n    Intro Git Tutorial\n    Git Status Tutorial\n"
        self.assertEqual(game.display_ground(), expected)

        change_location_file("Mountain Gate")

    def test_display_characters(self):
        change_location_file("Mountain Gate")

        game = GitCrystalsCmd()
        expected = 'There is no here but you\n'
        self.assertEqual(game.display_characters(), expected)

        change_location_file("Dragon's Lair")
        game = GitCrystalsCmd()
        expected = "In Dragon's Lair you see...\n    princess\n    grandfather\n    dragon\n"
        self.assertEqual(game.display_characters(), expected)

        change_location_file("Mountain Gate")

    def test_create_character(self):
        change_location_file("Mountain Gate")
        game = GitCrystalsCmd()
        player = game.player
        self.assertEqual(player.js_location.data['location'], "Mountain Gate")
        princess = game.create_character('princess')
        self.assertEqual(princess.js_location.data['location'], "Dragon's Lair")

    def test_go(self):
        change_location_file("Mountain Gate")
        game = GitCrystalsCmd()
        game.do_go('north')
        expected_location = "Git Crystal"
        player_location = game.player.location
        json_file = JsonData(repodir,"location")
        file_location = json_file.data['location']

        self.assertEqual(player_location, expected_location)
        self.assertEqual(file_location, expected_location)

        change_location_file("Mountain Gate")

    def test_do_look(self):
        game = GitCrystalsCmd()
        expected = """You are in Mountain Gate
To your north is... Git Crystal
To your south is... 
To your east is... 
To your west is... 
In Mountain Gate you see...
    No Trepassing Sign
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
    No Trepassing Sign
"""

        game.do_look('ground')
        self.assertEqual(game.output, expected)

        expected = """There is no here but you
"""
        game.do_look('people')
        self.assertEqual(game.output, expected)

    def test_do_take(self):
        game = GitCrystalsCmd()
        game.do_take('No Trepassing Sign')
        expected_inventory = game.player.js_inventory.data['items']
        self.assertListEqual(['Distress Note', 'No Trepassing Sign'], expected_inventory)
        item = game.player.js_inventory.data['items'].pop(1)
        game.player.js_inventory.write()
        game.world_map.rooms.data['Mountain Gate']['ground'].append(item)
        game.world_map.rooms.write()

if __name__ == '__main__':
    unittest.main()
