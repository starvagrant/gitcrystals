#!/usr/bin/env python3

from project.jsondata import JsonData
import unittest
from collections import OrderedDict

class Tests(unittest.TestCase):

    def test_jsondata_load(self):
        inventory = JsonData('game-repo','inventory')
        inv_list = [("Basic Clothes", 1),("Git Gem", 1),("Distress Note", 1)]
        expected_dict = OrderedDict(inv_list)
        self.assertDictEqual(inventory.data, expected_dict)

    def test_jsondata_write(self):
        alive = JsonData('game-repo','alive')
        alive.data['alive'] = False
        alive.write()

        f = open('game-repo/alive.json', 'r')
        text = f.read()
        f.close()

        alive.data['alive'] = True
        alive.write()

        self.assertEqual(text, '{\n    "alive":false\n}\n\n')

if __name__ == '__main__':
    unittest.main()
