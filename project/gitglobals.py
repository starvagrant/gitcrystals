#!/usr/bin/env python3
import project.command_wrapper as cw
import os
from project.jsondata import JsonData

# Constants
GIT = 'git'
GIT_DIR = '--git-dir=game-repo/.git'
WORK_TREE = '--work-tree=./game-repo'
TEST_REPO = 'game-repo'

# Test Repo Dependendencies

current_commit_sha='15946db05563105bc391b8bcb2c8e93eaa4506bd'
current_branch='data'
repodir="game-repo"
# Command Functions

def reset_repo():
    command = [GIT, '-C',repodir,'checkout',current_branch]
    process = cw.run_process(command)

    command = [GIT, '-C',repodir,'reset','--hard', current_commit_sha]
    process = cw.run_process(command)

    branches = []
    command = [GIT, '-C',repodir,'--show-ref', '--heads']
    process = cw.run_process(command)
    output = process.stdout
    output_lines = output.split('\n')
    if '' in output_lines:
        output_lines.pop()
    for line in output_lines:
        branches.append(re.sub(r'[0-9a-f]{40} refs/heads/','', line))
    for branch in branches:
        if branch != 'data':
            command = [G.GIT, '-C',repodir,'branch','-D', branch]
            process = cw.run_process(command)

def test_clean_repo():
    command = [GIT, '-C', repodir, 'rev-list', current_branch]
    process = cw.run_process(command)
    output = process.stdout
    if not output.split('\n')[0]==current_commit_sha:
        raise Exception("Extra commits found in test repository, please reset")

    command = [GIT, '-C', repodir, 'status', '--short']
    process = cw.run_process(command)
    output = process.stdout
    if not output=='':
        raise Exception("Working Directory or Index Not Clean. Please clear")

    command = [GIT, '-C', repodir, 'show-ref', '--heads']
    process = cw.run_process(command)
    output = process.stdout
    lines = output.split('\n')
    if len(lines) > 2: # only one ref
        raise Exception("Unnecessary Branches, Please Delete")

    return True

def change_location_file(new_location):
    json_file = JsonData(repodir,"location")
    json_file.data['location'] = new_location
    json_file.write()

def change_character_info(character, attribute, value):
    json_file = JsonData(repodir + os.sep + character, attribute)
    json_file.data[attribute] = value
    json_file.write()
