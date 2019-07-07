#!/usr/bin/env python3

from project.jsondata import JsonData

class WorldMap():

    def __init__(self, dir_name='game-repo', name='world_rooms'):
        self.rooms = JsonData(dir_name,name)

    def get_direction(self, location, direction):
        return self.rooms.data[location].get(direction, '')

    def get_ground_items(self, location):
        return self.rooms.data[location].get('ground', [])

    def set_ground_items(self, location, item_list):
        self.rooms.data[location]['ground'] = item_list

if __name__ == '__main__':
    world_map = WorldMap()

    for direction in ["north","south","east","west"]:
        print(world_map.get_direction('Git Crystal', direction))
