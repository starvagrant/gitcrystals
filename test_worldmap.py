#!/usr/bin/env python3

import unittest
import worldmap

def return_key_error(direction):
    try:
        raise KeyError("Cannot Go " + direction)
    except KeyError as e:
        return e

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

        key_error=world_map.get_direction(room_names[0], 'north')
        expected_error = return_key_error('north')
        self.assertEqual(repr(key_error), repr(expected_error))

unittest.main()
