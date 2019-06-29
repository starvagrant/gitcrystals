#!/usr/bin/python3

import unittest
import character
from jsondata import JsonData
from character import Character

class Tests(unittest.TestCase):

    def test_is_player(self):
        json_files = []
        json_files.append(JsonData("game-repo","alive"))
        json_files.append(JsonData("game-repo","location"))
        json_files.append(JsonData("game-repo","inventory"))
        json_files.append(JsonData("game-repo","status"))
        player = Character(json_files)
        self.assertTrue(player.is_player)

    def test_is_not_player(self):
        json_files = []
        json_files.append(JsonData("game-repo/princess","alive"))
        json_files.append(JsonData("game-repo/princess","location"))
        json_files.append(JsonData("game-repo/princess","inventory"))
        json_files.append(JsonData("game-repo/princess","status"))
        json_files.append(JsonData("game-repo/princess","relationship"))
        princess = Character(json_files)
        self.assertFalse(princess.is_player)

unittest.main()
