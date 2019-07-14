#!/usr/bin/python3

from project.jsondata import JsonData
from project.character import Character
import unittest

class CJ():
    player_json_files = []
    player_json_files.append(JsonData("game-repo","alive"))
    player_json_files.append(JsonData("game-repo","location"))
    player_json_files.append(JsonData("game-repo","inventory"))
    player_json_files.append(JsonData("game-repo","status"))

    princess_json_files = []
    princess_json_files.append(JsonData("game-repo/princess","alive"))
    princess_json_files.append(JsonData("game-repo/princess","location"))
    princess_json_files.append(JsonData("game-repo/princess","inventory"))
    princess_json_files.append(JsonData("game-repo/princess","status"))
    princess_json_files.append(JsonData("game-repo/princess","relationship"))

class Tests(unittest.TestCase):

    def test_is_player(self):
        player = Character(CJ.player_json_files)
        self.assertTrue(player.is_player)

    def test_is_not_player(self):
        princess = Character(CJ.princess_json_files)
        self.assertFalse(princess.is_player)

    def test_attributes(self):
        player = Character(CJ.player_json_files)
        self.assertTrue(player.alive)
        self.assertEqual(player.location, "Mountain Gate")


if __name__ == '__main__':
    unittest.main()
