#!/usr/bin/env python3

import project.gitcrystals
import project.gitcli
from project.jsondata import JsonData

playing = True
alive_json = JsonData('game', 'alive')
game_intro = """    Welcome to Git Crystals!')
    ========================')

    Type "help" for commands.'
    Press Ctrl-C to Quit at Any Time
"""
git_intro = """     Welcome to Git Crystals!
    ========================')
    You are dead. Git Crystals
    is playing in Git Mode.
    Press Ctrl-C to Quit at Any Time
"""
death_message = """You died as a result of that action.
Game entering git only mode"""

revive_message = """Git Workflow Saved You From Death
Game entering normal mode"""

while playing:
    if alive_json.data['alive'] == True:
        game = project.gitcrystals.GitCrystalsCmd('game')
        print(game_intro)
        game.cmdloop()
        alive_json.load()
        if alive_json.data['alive'] == False:
            print(death_message)
        else:
            print("Game exited from game loop while character alive...?")
    else:
        game = project.gitcli.GitCmd('game')
        print(git_intro)
        game.cmdloop()
        alive_json.load()
        if alive_json.data['alive']:
            print(revive_message)
        else:
            print("Game exited from git loop while character dead...?")

    gameContinue = input('Continue Y/N?')
    if gameContinue.lower() == 'n':
        break
