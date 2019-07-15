#!/usr/bin/python3

from project.jsondata import JsonData
from project.character import Character
import unittest

def create_json_file(json_dir="game-repo", json_file="alive"):
    return JsonData(json_dir,json_file)

class Tests(unittest.TestCase):

    def setUp(self):
        alive = create_json_file("game-repo","alive")
        location = create_json_file("game-repo", "location")
        inventory = create_json_file("game-repo", "inventory")
        status = create_json_file("game-repo", "status")

        player_json_files = [alive, location, inventory, status]

        pr_alive = create_json_file("game-repo/princess","alive")
        pr_location = create_json_file("game-repo/princess", "location")
        pr_inventory = create_json_file("game-repo/princess", "inventory")
        pr_status = create_json_file("game-repo/princess", "status")
        pr_relationship = create_json_file("game-repo/princess", "relationship")

        princess_json_files = [pr_alive, pr_location, pr_inventory, pr_status, pr_relationship]

        self.player = Character(player_json_files)
        self.princess = Character(princess_json_files)

    def test_is_player(self):
        self.assertTrue(self.player.is_player)

    def test_is_not_player(self):
        self.assertFalse(self.princess.is_player)

    def test_attributes(self):
        self.assertTrue(self.player.alive)
        self.assertEqual(self.player.location, "Mountain Gate")

if __name__ == '__main__':
    unittest.main()
