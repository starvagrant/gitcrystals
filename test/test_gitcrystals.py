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

    def test_loop_exit(self):
        # A do_* method exits when it returns True.
        # Game loop should end when player is dead.
        game = GitCrystalsCmd()
        game.alive.data['alive'] = True
        game.alive.write()

        game_loop_exits1 = game.do_checkoutfile('alive.json')
        game_loop_exits2 = game.do_checkout('data')
        game_loop_exits3 = game.do_checkoutforce('data')
        game_loop_exits4 = game.do_merge('data')
        game_loop_exits5 = game.do_resolveleft('alive.json')
        game_loop_exits6 = game.do_resolveright('alive.json')

        self.assertFalse(game_loop_exits1)
        self.assertFalse(game_loop_exits2)
        self.assertFalse(game_loop_exits3)
        self.assertFalse(game_loop_exits4)
        self.assertFalse(game_loop_exits5)
        self.assertFalse(game_loop_exits6)

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
        expected = 'There is no here but you.\n'
        self.assertEqual(game.display_characters(), expected)

        G.change_location_file("Dragon's Lair")
        game = GitCrystalsCmd()
        expected = "In Dragon's Lair you see...\n    princess\n    grandfather\n    dragon\n"
        self.assertEqual(game.display_characters(), expected)

        G.change_location_file("Mountain Gate")

    def test_display_inventory(self):
        game = GitCrystalsCmd()
        expected = "You have: \n1 of Basic Clothes\n1 of Distress Note\n1 of Git Gem\n"
        self.assertEqual(game.display_inventory(), expected)

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
        line = 'go north'
        stop = game.onecmd(line)
        game.postcmd(stop, line)
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
There is no here but you.
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

        expected = """There is no here but you.\n"""
        game.do_look('people')
        self.assertEqual(game.output, expected)

    def test_do_take(self):
        game = GitCrystalsCmd()

        line = 'take No Trespassing Sign'
        stop = game.onecmd(line)
        game.postcmd(stop, line)

        inventory_list = [("Basic Clothes",1),("Distress Note",1),("Git Gem",1),("No Trespassing Sign",1)]
        actual_inventory = game.player.js_inventory.data
        expected_inventory = OrderedDict(inventory_list)
        self.assertEqual(actual_inventory, expected_inventory)

        line = 'drop No Trespassing Sign'
        stop = game.onecmd(line)
        game.postcmd(stop, line)

    def test_do_drop(self):
        game = GitCrystalsCmd()

        line = 'take No Trespassing Sign'
        stop = game.onecmd(line)
        game.postcmd(stop, line)
        line = 'drop No Trespassing Sign'
        stop = game.onecmd(line)
        game.postcmd(stop, line)

        actual_inventory = game.player.js_inventory.data
        inventory_list = [("Basic Clothes",1),("Distress Note",1),("Git Gem",1)]
        expected_inventory = OrderedDict(inventory_list)
        self.assertEqual(actual_inventory, expected_inventory)

    def test_do_search(self):
        game = GitCrystalsCmd()
        game.do_search('')
        expected = """In Mountain Gate you see...
    No Trespassing Sign
"""
        self.assertEqual(expected, game.output)

    def test_do_perilious_search(self):
        G.change_location_file("Abandoned Treasury")
        game = GitCrystalsCmd()
        line = 'search'
        stop = game.onecmd(line)
        game.postcmd(stop, line)
        expected = """In Abandoned Treasury you see...
    Charcoal
    Treasure Chest Key
"""
        output = game.output
        alive = game.player.js_alive.data['alive']
        game.do_checkoutfile('alive.json')
        game.do_checkoutfile('location.json')

        self.assertEqual(expected, output)
        self.assertFalse(alive)

    def test_do_perilious_search_with_others(self):
        G.change_location_file("Abandoned Treasury")
        G.change_character_info('princess', 'location', 'Abandoned Treasury')
        game = GitCrystalsCmd()

        line = 'search'
        stop = game.onecmd(line)
        game.postcmd(stop, line)

        output = game.output
        alive = game.player.js_alive.data['alive']
        princess_alive = game.characters['princess'].js_alive.data['alive']

        expected = """In Abandoned Treasury you see...
    Charcoal
    Treasure Chest Key\n"""

        game.do_checkoutfile('alive.json')
        game.do_checkoutfile('location.json')
        game.do_checkoutfile('princess/location.json')

        self.assertEqual(expected, output)
        self.assertFalse(alive)
        self.assertFalse(princess_alive)

    def test_do_checkoutfile(self):
        game = GitCrystalsCmd()
        game.do_north('')
        game.do_checkoutfile('location.json')
        expected = 'Mountain Gate'
        self.assertEqual(game.player.location, expected)

    def test_load_data(self):
        game = GitCrystalsCmd()
        G.change_location_file('Git Crystal')
        game.load_data()
        expected = 'Git Crystal'
        self.assertEqual(game.player.location, expected)

    def test_write_data(self):
        game = GitCrystalsCmd()
        G.change_location_file('Git Crystal')
        game.load_data()
        G.change_location_file('Mountain Gate')
        game.write_data()
        file_data = JsonData(G.repodir, "location")
        self.assertEqual(file_data.data['location'], 'Git Crystal')

if __name__ == '__main__':
    unittest.main()
