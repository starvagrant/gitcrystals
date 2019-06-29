#!/usr/bin/env python3

import jsondata

class WorldMap():

    def __init__(self, dir_name='game-repo', name='world_rooms'):
        self.rooms = jsondata.JsonData(dir_name,name)

    def get_direction(self, location, direction):
        return self.rooms.data[location].get(direction, None)

if __name__ == '__main__':
    world_map = WorldMap()

    for direction in ["north","south","east","west"]:
        print(world_map.get_direction('Git Crystal', direction))
