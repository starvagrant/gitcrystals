#!/usr/bin/env python3

import unittest
import worldmap

class R():
    room_names = []
    world_map = worldmap.WorldMap()
    for key in world_map.rooms.data.keys():
        room_names.append(key)

class Tests(unittest.TestCase):

    def test_get_north(self):
        world_map = worldmap.WorldMap()
        new_room=world_map.get_direction(R.room_names[1], 'north')
        expected_room = "Abandoned Treasury"
        self.assertEqual(new_room, expected_room)

    def test_get_invalid_north(self):
        world_map = worldmap.WorldMap()
        no_room=world_map.get_direction(R.room_names[0], 'north')
        self.assertEquals(no_room, '')

unittest.main()
