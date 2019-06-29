#!/usr/bin/env python3

import unittest
import worldmap

class Tests(unittest.TestCase):

    def test_get_north(self):
        room_names = []
        world_map = worldmap.WorldMap()
        for key in world_map.rooms.data.keys():
            room_names.append(key)

        new_room=world_map.get_direction(room_names[1], 'north')
        expected_room = "Abandoned Treasury"
        self.assertEqual(new_room, expected_room)

    def test_get_invalid_north(self):
        room_names = []
        world_map = worldmap.WorldMap()
        for key in world_map.rooms.data.keys():
            room_names.append(key)

        no_room=world_map.get_direction(room_names[0], 'north')
        self.assertIsNone(no_room)

unittest.main()
