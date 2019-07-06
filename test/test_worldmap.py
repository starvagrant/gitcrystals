#!/usr/bin/env python3

import unittest
import worldmap

class Tests(unittest.TestCase):

    def test_get_north(self):
        world_map = worldmap.WorldMap()
        new_room=world_map.get_direction("Alchemist Lab", 'north')
        expected_room = "Abandoned Treasury"
        self.assertEqual(new_room, expected_room)

    def test_get_invalid_north(self):
        world_map = worldmap.WorldMap()
        no_room=world_map.get_direction("Abandoned Treasury", 'north')
        self.assertEqual(no_room, '')

    def test_get_ground_items(self):
        world_map = worldmap.WorldMap()
        ground_items = world_map.get_ground_items("Git Crystal")
        expected = ["Intro Git Tutorial","Git Status Tutorial"]
        self.assertListEqual(ground_items, expected)

    def test_empty_ground_items(self):
        world_map = worldmap.WorldMap()
        world_map.rooms.data['Mountain Gate'].pop('ground') # Simulate a room without ground key
        ground_items = world_map.get_ground_items("Mountain Gate")
        expected = []
        self.assertListEqual(ground_items, expected)

unittest.main()
