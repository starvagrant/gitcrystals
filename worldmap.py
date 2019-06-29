#!/usr/bin/env python3

import jsondata

class WorldMap():

    def __init__(self, dir_name='game-repo', name='world_rooms'):
        self.rooms = jsondata.JsonData(dir_name,name)

    def get_direction(self, location, direction):
        """ location is current room location.
            direction is north, south, east, west."""
        try:
            if location not in self.rooms.data.keys():
                raise KeyError("Not a valid location")
            if direction not in self.rooms.data[location].keys():
                raise KeyError("Cannot Go " + direction)
        except KeyError as e:
            return e

        return self.rooms.data[location][direction]


if __name__ == '__main__':
    world_map = WorldMap()

    for direction in ["north","south","east","west"]:
        print(world_map.get_direction('Git Crystal', direction))
