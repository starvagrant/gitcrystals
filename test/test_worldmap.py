#!/usr/bin/env python3

from project.worldmap import WorldMap
import unittest
from collections import OrderedDict

class Tests(unittest.TestCase):

    def test_get_north(self):
        world_map = WorldMap()
        new_room=world_map.get_direction("Alchemist Lab", 'north')
        expected_room = "Abandoned Treasury"
        self.assertEqual(new_room, expected_room)

    def test_get_invalid_north(self):
        world_map = WorldMap()
        no_room=world_map.get_direction("Abandoned Treasury", 'north')
        self.assertEqual(no_room, '')

    def test_get_ground_items(self):
        world_map = WorldMap()
        ground_items = world_map.get_ground_items("Git Crystal")
        inv_list = [("Intro Git Tutorial",1),("Git Status Tutorial", 1)]
        expected = OrderedDict(inv_list)
        self.assertDictEqual(ground_items, expected)

    def test_empty_ground_items(self):
        world_map = WorldMap()
        world_map.rooms.data['Mountain Gate'].pop('ground') # Simulate a room without ground key
        ground_items = world_map.get_ground_items("Mountain Gate")
        expected = OrderedDict()
        self.assertDictEqual(ground_items, expected)

if __name__ == '__main__':
    unittest.main()
